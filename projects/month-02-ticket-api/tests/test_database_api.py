from collections.abc import Iterator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, func, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from ticket_api.database import create_session_factory
from ticket_api.dependencies import SessionDependency
from ticket_api.main import create_app
from ticket_api.passwords import PasswordHasher
from ticket_api.persistence_models import TicketRecord, UserRecord

pytestmark = pytest.mark.integration


class CommitFailingSession(Session):
    def commit(self) -> None:
        raise RuntimeError("forced commit failure")


@pytest.fixture
def postgresql_api_client(
    postgresql_test_engine: Engine,
) -> Iterator[TestClient]:
    application = create_app(lifespan_handler=None)
    application.state.session_factory = create_session_factory(postgresql_test_engine)

    @application.post(
        "/__test__/rollback",
        include_in_schema=False,
    )
    def rollback_probe(
        title: str,
        session: SessionDependency,
    ) -> None:
        record = TicketRecord(
            title=title,
            priority="low",
        )
        session.add(record)
        session.flush()

        raise RuntimeError("forced rollback probe")

    with TestClient(application) as client:
        yield client


@pytest.fixture
def postgresql_commit_failure_client(
    postgresql_test_engine: Engine,
) -> Iterator[TestClient]:
    application = create_app(lifespan_handler=None)

    application.state.session_factory = sessionmaker(
        bind=postgresql_test_engine,
        class_=CommitFailingSession,
        autoflush=False,
        expire_on_commit=False,
    )

    with TestClient(
        application,
        raise_server_exceptions=False,
    ) as client:
        yield client


def test_created_ticket_is_committed_and_readable_in_later_request(
    postgresql_api_client: TestClient,
    postgresql_test_engine: Engine,
) -> None:
    with postgresql_test_engine.connect() as connection:
        ticket_count = connection.scalar(select(func.count()).select_from(TicketRecord))

    assert ticket_count == 0

    title = f"API commit probe {uuid4().hex}"

    try:
        response = postgresql_api_client.post(
            "/tickets",
            json={"title": title, "priority": "high"},
        )
        assert response.status_code == 201

        data = response.json()
        ticket_id = data["ticket_id"]

        assert ticket_id > 0
        assert data["title"] == title
        assert data["priority"] == "high"
        assert data["status"] == "open"

        with postgresql_test_engine.connect() as connection:
            statement = select(TicketRecord.title).where(
                TicketRecord.ticket_id == ticket_id
            )
            db_title = connection.scalar(statement)

        assert db_title == title

        get_response = postgresql_api_client.get(f"/tickets/{ticket_id}")
        assert get_response.status_code == 200
        assert get_response.json() == data

    finally:
        with postgresql_test_engine.begin() as connection:
            connection.execute(delete(TicketRecord).where(TicketRecord.title == title))


def test_list_tickets_filters_status_and_respects_limit_with_postgresql(
    postgresql_api_client: TestClient,
    postgresql_test_engine: Engine,
) -> None:
    marker = uuid4().hex
    titles = [
        f"First list probe {marker}",
        f"Second list probe {marker}",
        f"Resolved list probe {marker}",
    ]

    with postgresql_test_engine.connect() as connection:
        ticket_count = connection.scalar(select(func.count()).select_from(TicketRecord))

    assert ticket_count == 0

    try:
        created_tickets = []
        for title in titles:
            response = postgresql_api_client.post(
                "/tickets",
                json={"title": title, "priority": "medium"},
            )
            assert response.status_code == 201
            created_tickets.append(response.json())

        third_ticket_id = created_tickets[2]["ticket_id"]
        patch_response = postgresql_api_client.patch(
            f"/tickets/{third_ticket_id}",
            json={"status": "resolved"},
        )
        assert patch_response.status_code == 200
        assert patch_response.json()["status"] == "resolved"

        open_list_response = postgresql_api_client.get(
            "/tickets", params={"status": "open", "limit": 10}
        )
        assert open_list_response.status_code == 200
        open_tickets = open_list_response.json()
        assert [ticket["title"] for ticket in open_tickets] == titles[:2]

        limit_list_response = postgresql_api_client.get("/tickets", params={"limit": 1})
        assert limit_list_response.status_code == 200
        limit_tickets = limit_list_response.json()
        assert len(limit_tickets) == 1
        assert limit_tickets[0]["title"] == titles[0]

    finally:
        with postgresql_test_engine.begin() as connection:
            connection.execute(
                delete(TicketRecord).where(TicketRecord.title.in_(titles))
            )


def test_update_and_delete_are_committed_across_postgresql_requests(
    postgresql_api_client: TestClient,
    postgresql_test_engine: Engine,
) -> None:
    marker = uuid4().hex
    original_title = f"Update lifecycle probe {marker}"
    updated_title = f"Updated lifecycle probe {marker}"

    ticket_id: int | None = None

    try:
        post_response = postgresql_api_client.post(
            "/tickets",
            json={"title": original_title, "priority": "low"},
        )
        assert post_response.status_code == 201
        ticket_id = post_response.json()["ticket_id"]

        patch_payload = {
            "title": updated_title,
            "priority": "critical",
            "status": "in_progress",
        }
        patch_response = postgresql_api_client.patch(
            f"/tickets/{ticket_id}",
            json=patch_payload,
        )
        assert patch_response.status_code == 200
        patch_data = patch_response.json()
        assert patch_data["ticket_id"] == ticket_id
        assert patch_data["title"] == updated_title
        assert patch_data["priority"] == "critical"
        assert patch_data["status"] == "in_progress"

        with postgresql_test_engine.connect() as connection:
            statement = select(
                TicketRecord.title,
                TicketRecord.priority,
                TicketRecord.status,
            ).where(TicketRecord.ticket_id == ticket_id)

            db_title, db_priority, db_status = connection.execute(statement).one()

        assert db_title == updated_title
        assert db_priority == "critical"
        assert db_status == "in_progress"

        get_response = postgresql_api_client.get(f"/tickets/{ticket_id}")
        assert get_response.status_code == 200
        assert get_response.json() == patch_data

        delete_response = postgresql_api_client.delete(f"/tickets/{ticket_id}")
        assert delete_response.status_code == 204
        assert delete_response.content == b""

        with postgresql_test_engine.connect() as connection:
            count_statement = (
                select(func.count())
                .select_from(TicketRecord)
                .where(TicketRecord.ticket_id == ticket_id)
            )
            db_count = connection.scalar(count_statement)

        assert db_count == 0

        get_deleted_response = postgresql_api_client.get(f"/tickets/{ticket_id}")
        assert get_deleted_response.status_code == 404
        assert get_deleted_response.json() == {
            "detail": f"Ticket {ticket_id} not found"
        }

    finally:
        if ticket_id is not None:
            with postgresql_test_engine.begin() as connection:
                connection.execute(
                    delete(TicketRecord).where(TicketRecord.ticket_id == ticket_id)
                )


def test_missing_ticket_requests_return_404_without_database_changes(
    postgresql_api_client: TestClient,
    postgresql_test_engine: Engine,
) -> None:
    missing_ticket_id = 2**63 - 1

    with postgresql_test_engine.connect() as connection:
        ticket_count = connection.scalar(select(func.count()).select_from(TicketRecord))

    assert ticket_count == 0

    get_response = postgresql_api_client.get(f"/tickets/{missing_ticket_id}")
    patch_response = postgresql_api_client.patch(
        f"/tickets/{missing_ticket_id}",
        json={"status": "closed"},
    )
    delete_response = postgresql_api_client.delete(f"/tickets/{missing_ticket_id}")

    for response in (get_response, patch_response, delete_response):
        assert response.status_code == 404
        assert response.json() == {"detail": f"Ticket {missing_ticket_id} not found"}

    with postgresql_test_engine.connect() as connection:
        ticket_count_after = connection.scalar(
            select(func.count()).select_from(TicketRecord)
        )

    assert ticket_count_after == 0


def test_invalid_requests_return_422_without_database_changes(
    postgresql_api_client: TestClient,
    postgresql_test_engine: Engine,
) -> None:
    invalid_title = f"Invalid request probe {uuid4().hex}"

    try:
        invalid_create_response = postgresql_api_client.post(
            "/tickets",
            json={
                "title": invalid_title,
                "priority": "urgent",
            },
        )

        empty_patch_response = postgresql_api_client.patch(
            f"/tickets/{2**63 - 1}",
            json={},
        )

        invalid_filter_response = postgresql_api_client.get(
            "/tickets",
            params={"status": "unknown"},
        )

        for response in (
            invalid_create_response,
            empty_patch_response,
            invalid_filter_response,
        ):
            assert response.status_code == 422

        assert invalid_create_response.json()["detail"][0]["loc"] == [
            "body",
            "priority",
        ]

        assert empty_patch_response.json()["detail"][0]["loc"] == [
            "body",
        ]

        assert invalid_filter_response.json()["detail"][0]["loc"] == [
            "query",
            "status",
        ]

        with postgresql_test_engine.connect() as connection:
            ticket_count = connection.scalar(
                select(func.count()).select_from(TicketRecord)
            )

        assert ticket_count == 0

    finally:
        with postgresql_test_engine.begin() as connection:
            connection.execute(
                delete(TicketRecord).where(TicketRecord.title == invalid_title)
            )


def test_request_error_rolls_back_flushed_postgresql_write(
    postgresql_api_client: TestClient,
    postgresql_test_engine: Engine,
) -> None:
    with postgresql_test_engine.connect() as connection:
        ticket_count = connection.scalar(select(func.count()).select_from(TicketRecord))

    assert ticket_count == 0

    title = f"Rollback request probe {uuid4().hex}"

    try:
        with pytest.raises(RuntimeError, match="forced rollback probe"):
            postgresql_api_client.post(
                "/__test__/rollback",
                params={"title": title},
            )

        with postgresql_test_engine.connect() as connection:
            statement = (
                select(func.count())
                .select_from(TicketRecord)
                .where(TicketRecord.title == title)
            )
            matching_count = connection.scalar(statement)
            total_count = connection.scalar(
                select(func.count()).select_from(TicketRecord)
            )

        assert matching_count == 0
        assert total_count == 0

    finally:
        with postgresql_test_engine.begin() as connection:
            connection.execute(delete(TicketRecord).where(TicketRecord.title == title))


def test_commit_failure_prevents_201_and_rolls_back_postgresql_write(
    postgresql_commit_failure_client: TestClient,
    postgresql_test_engine: Engine,
) -> None:
    title = f"Commit failure probe {uuid4().hex}"

    try:
        response = postgresql_commit_failure_client.post(
            "/tickets",
            json={
                "title": title,
                "priority": "high",
            },
        )

        assert response.status_code == 500
        assert response.text == "Internal Server Error"

        with postgresql_test_engine.connect() as connection:
            matching_statement = (
                select(func.count())
                .select_from(TicketRecord)
                .where(TicketRecord.title == title)
            )
            matching_count = connection.scalar(matching_statement)
            total_count = connection.scalar(
                select(func.count()).select_from(TicketRecord)
            )

        assert matching_count == 0
        assert total_count == 0

    finally:
        with postgresql_test_engine.begin() as connection:
            connection.execute(delete(TicketRecord).where(TicketRecord.title == title))


def test_each_postgresql_request_uses_a_distinct_session(
    postgresql_test_engine: Engine,
) -> None:
    with postgresql_test_engine.connect() as connection:
        ticket_count = connection.scalar(select(func.count()).select_from(TicketRecord))

    assert ticket_count == 0

    created_sessions: list[Session] = []
    real_session_factory = create_session_factory(postgresql_test_engine)

    def tracking_session_factory() -> Session:
        session = real_session_factory()
        created_sessions.append(session)
        return session

    application = create_app(lifespan_handler=None)
    application.state.session_factory = tracking_session_factory

    with TestClient(application) as client:
        first_response = client.get("/tickets")
        second_response = client.get("/tickets")

    assert first_response.status_code == 200
    assert first_response.json() == []

    assert second_response.status_code == 200
    assert second_response.json() == []

    assert len(created_sessions) == 2
    assert created_sessions[0] is not created_sessions[1]

    with postgresql_test_engine.connect() as connection:
        ticket_count_after = connection.scalar(
            select(func.count()).select_from(TicketRecord)
        )

    assert ticket_count_after == 0


def test_registered_user_is_committed_with_hashed_password(
    postgresql_api_client: TestClient,
    postgresql_test_engine: Engine,
) -> None:
    marker = uuid4().hex
    email = f"registration-{marker}@example.com"
    plain_password = "strong-password-123"

    try:
        response = postgresql_api_client.post(
            "/auth/register",
            json={
                "email": email,
                "password": plain_password,
            },
        )

        assert response.status_code == 201

        response_data = response.json()
        assert response_data["email"] == email
        assert response_data["role"] == "member"
        assert response_data["is_active"] is True
        assert "password" not in response_data
        assert "password_hash" not in response_data

        with postgresql_test_engine.connect() as connection:
            password_hash = connection.scalar(
                select(UserRecord.password_hash).where(UserRecord.email == email)
            )

        assert isinstance(password_hash, str)
        assert password_hash != plain_password
        assert password_hash.startswith("$argon2id$")
        assert PasswordHasher().verify_password(
            plain_password,
            password_hash,
        )

    finally:
        with postgresql_test_engine.begin() as connection:
            connection.execute(delete(UserRecord).where(UserRecord.email == email))


def test_duplicate_registration_returns_409_and_preserves_original_user(
    postgresql_api_client: TestClient,
    postgresql_test_engine: Engine,
) -> None:
    marker = uuid4().hex
    normalized_email = f"duplicate-{marker}@example.com"
    password = "strong-password-123"

    try:
        first_response = postgresql_api_client.post(
            "/auth/register",
            json={
                "email": f"Duplicate-{marker}@Example.COM",
                "password": password,
            },
        )
        assert first_response.status_code == 201
        assert first_response.json()["email"] == normalized_email

        duplicate_response = postgresql_api_client.post(
            "/auth/register",
            json={
                "email": normalized_email,
                "password": password,
            },
        )
        assert duplicate_response.status_code == 409
        assert duplicate_response.json() == {"detail": "User registration conflict"}

        with postgresql_test_engine.connect() as connection:
            user_count = connection.scalar(
                select(func.count())
                .select_from(UserRecord)
                .where(UserRecord.email == normalized_email)
            )

        assert user_count == 1

    finally:
        with postgresql_test_engine.begin() as connection:
            connection.execute(
                delete(UserRecord).where(UserRecord.email == normalized_email)
            )
