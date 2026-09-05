import pytest
from sqlalchemy import delete, func, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from ticket_api.database import create_session_factory
from ticket_api.models import (
    NewTicket,
    Ticket,
    TicketPriority,
    TicketStatus,
)
from ticket_api.persistence_models import TicketRecord, UserRecord
from ticket_api.repositories import UserRepositoryConflictError
from ticket_api.sqlalchemy_repositories import (
    SqlAlchemyTicketRepository,
    SqlAlchemyUserRepository,
)
from ticket_api.user_models import NewUser, UserRole

pytestmark = pytest.mark.integration


def assert_ticket_table_is_empty(engine: Engine) -> None:
    with engine.connect() as connection:
        ticket_count = connection.scalar(select(func.count()).select_from(TicketRecord))

    assert ticket_count == 0


def create_ticket_owner(session: Session) -> int:
    repository = SqlAlchemyUserRepository(session)
    user = repository.create(
        NewUser(
            email="ticket-owner@example.com",
            password_hash="$argon2id$ticket-owner-example",
        )
    )
    return user.user_id


@pytest.fixture
def ticket_owner_id(database_session: Session) -> int:
    return create_ticket_owner(database_session)


def test_committed_ticket_is_visible_in_new_session(
    postgresql_test_engine: Engine,
) -> None:
    assert_ticket_table_is_empty(postgresql_test_engine)

    session_factory = create_session_factory(postgresql_test_engine)
    ticket_id: int | None = None
    owner_id: int | None = None

    try:
        with session_factory() as write_session:
            owner_id = create_ticket_owner(write_session)
            repository = SqlAlchemyTicketRepository(write_session)
            created_ticket = repository.create(
                NewTicket(
                    title="Committed database ticket",
                    priority=TicketPriority.HIGH,
                    owner_id=owner_id,
                )
            )
            ticket_id = created_ticket.ticket_id

            write_session.commit()

        with session_factory() as read_session:
            repository = SqlAlchemyTicketRepository(read_session)
            stored_ticket = repository.get_by_id(ticket_id)

            assert stored_ticket == created_ticket
    finally:
        with postgresql_test_engine.begin() as connection:
            if ticket_id is not None:
                connection.execute(
                    delete(TicketRecord).where(TicketRecord.ticket_id == ticket_id)
                )
            if owner_id is not None:
                connection.execute(
                    delete(UserRecord).where(UserRecord.user_id == owner_id)
                )


def test_rolled_back_ticket_is_not_visible_in_new_session(
    postgresql_test_engine: Engine,
) -> None:
    assert_ticket_table_is_empty(postgresql_test_engine)

    session_factory = create_session_factory(postgresql_test_engine)

    with session_factory() as write_session:
        owner_id = create_ticket_owner(write_session)
        repository = SqlAlchemyTicketRepository(write_session)
        created_ticket = repository.create(
            NewTicket(
                title="Rolled back database ticket",
                priority=TicketPriority.LOW,
                owner_id=owner_id,
            )
        )

        write_session.rollback()

    with session_factory() as read_session:
        repository = SqlAlchemyTicketRepository(read_session)

        assert repository.get_by_id(created_ticket.ticket_id) is None


def test_repository_update_advances_updated_at(
    postgresql_test_engine: Engine,
) -> None:
    assert_ticket_table_is_empty(postgresql_test_engine)

    session_factory = create_session_factory(postgresql_test_engine)
    ticket_id: int | None = None
    owner_id: int | None = None

    try:
        with session_factory() as create_session:
            owner_id = create_ticket_owner(create_session)
            repository = SqlAlchemyTicketRepository(create_session)
            ticket = repository.create(
                NewTicket(
                    title="Timestamp integration ticket",
                    priority=TicketPriority.MEDIUM,
                    owner_id=owner_id,
                )
            )
            ticket_id = ticket.ticket_id
            create_session.commit()

        with session_factory() as update_session:
            repository = SqlAlchemyTicketRepository(update_session)
            stored_ticket = repository.get_by_id(ticket_id)

            assert stored_ticket is not None

            stored_ticket.change_title("Updated timestamp integration ticket")

            assert repository.update(stored_ticket) is True

            update_session.commit()

        with session_factory() as verification_session:
            record = verification_session.get(TicketRecord, ticket_id)

            assert record is not None
            assert record.updated_at > record.created_at
    finally:
        with postgresql_test_engine.begin() as connection:
            if ticket_id is not None:
                connection.execute(
                    delete(TicketRecord).where(TicketRecord.ticket_id == ticket_id)
                )
            if owner_id is not None:
                connection.execute(
                    delete(UserRecord).where(UserRecord.user_id == owner_id)
                )


def test_repository_creates_database_generated_ticket(
    database_session: Session,
    ticket_owner_id: int,
) -> None:
    repository = SqlAlchemyTicketRepository(database_session)

    ticket = repository.create(
        NewTicket(
            title="  Database integration ticket  ",
            priority=TicketPriority.HIGH,
            owner_id=ticket_owner_id,
        )
    )

    assert ticket.ticket_id > 0
    assert ticket.owner_id == ticket_owner_id
    assert ticket.title == "Database integration ticket"
    assert ticket.priority is TicketPriority.HIGH
    assert ticket.status is TicketStatus.OPEN
    assert database_session.in_transaction() is True

    record = database_session.get(TicketRecord, ticket.ticket_id)
    assert record is not None
    assert record.owner_id == ticket_owner_id


def test_repository_gets_existing_ticket(
    database_session: Session,
    ticket_owner_id: int,
) -> None:
    repository = SqlAlchemyTicketRepository(database_session)
    ticket = repository.create(
        NewTicket(
            title="Existing database ticket",
            priority=TicketPriority.MEDIUM,
            owner_id=ticket_owner_id,
        )
    )

    fetched_ticket = repository.get_by_id(ticket.ticket_id)

    assert fetched_ticket == ticket


def test_repository_returns_none_for_missing_ticket(database_session: Session) -> None:
    repository = SqlAlchemyTicketRepository(database_session)

    fetched_ticket = repository.get_by_id(9_000_000_000)

    assert fetched_ticket is None


def test_repository_lists_only_owner_tickets_in_id_order(
    database_session: Session,
    ticket_owner_id: int,
) -> None:
    repository = SqlAlchemyTicketRepository(database_session)

    other_owner = SqlAlchemyUserRepository(database_session).create(
        NewUser(
            email="other-ticket-owner@example.com",
            password_hash="$argon2id$other-ticket-owner-example",
        )
    )

    first_owned_ticket = repository.create(
        NewTicket(
            title="First owned ticket",
            priority=TicketPriority.LOW,
            owner_id=ticket_owner_id,
        )
    )

    repository.create(
        NewTicket(
            title="Other user's ticket",
            priority=TicketPriority.MEDIUM,
            owner_id=other_owner.user_id,
        )
    )

    second_owned_ticket = repository.create(
        NewTicket(
            title="Second owned ticket",
            priority=TicketPriority.HIGH,
            owner_id=ticket_owner_id,
        )
    )

    tickets = repository.list_by_owner(ticket_owner_id)

    assert tickets == [
        first_owned_ticket,
        second_owned_ticket,
    ]


def test_repository_updates_ticket(
    database_session: Session,
    ticket_owner_id: int,
) -> None:
    repository = SqlAlchemyTicketRepository(database_session)
    ticket = repository.create(
        NewTicket(
            title="Initial database ticket",
            priority=TicketPriority.LOW,
            owner_id=ticket_owner_id,
        )
    )

    ticket.change_title("Updated database ticket")
    ticket.change_priority(TicketPriority.CRITICAL)
    ticket.change_status(TicketStatus.RESOLVED)

    assert repository.update(ticket) is True

    database_session.expire_all()
    stored_ticket = repository.get_by_id(ticket.ticket_id)

    assert stored_ticket == ticket


def test_repository_returns_false_when_updating_missing_ticket(
    database_session: Session,
) -> None:
    repository = SqlAlchemyTicketRepository(database_session)
    missing_ticket = Ticket(
        ticket_id=9_000_000_000,
        title="Missing database ticket",
        priority=TicketPriority.LOW,
        owner_id=7,
    )

    assert repository.update(missing_ticket) is False


def test_repository_deletes_ticket(
    database_session: Session,
    ticket_owner_id: int,
) -> None:
    repository = SqlAlchemyTicketRepository(database_session)
    ticket = repository.create(
        NewTicket(
            title="To be deleted ticket",
            priority=TicketPriority.LOW,
            owner_id=ticket_owner_id,
        )
    )

    assert repository.delete(ticket.ticket_id) is True
    assert repository.get_by_id(ticket.ticket_id) is None
    assert repository.delete(ticket.ticket_id) is False


def test_repository_does_not_commit_created_ticket(
    database_session: Session,
    postgresql_test_engine: Engine,
    ticket_owner_id: int,
) -> None:
    repository = SqlAlchemyTicketRepository(database_session)

    ticket = repository.create(
        NewTicket(
            title="Uncommitted database ticket",
            priority=TicketPriority.LOW,
            owner_id=ticket_owner_id,
        )
    )

    with postgresql_test_engine.connect() as connection:
        visible_ticket_id = connection.scalar(
            select(TicketRecord.ticket_id).where(
                TicketRecord.ticket_id == ticket.ticket_id
            )
        )

    assert visible_ticket_id is None


def test_user_repository_creates_database_generated_member(
    database_session: Session,
) -> None:
    repository = SqlAlchemyUserRepository(database_session)

    user = repository.create(
        NewUser(
            email=" Database.User@Example.com ",
            password_hash="$argon2id$integration-example",
        )
    )

    assert user.user_id > 0
    assert user.email == "database.user@example.com"
    assert user.password_hash == "$argon2id$integration-example"
    assert user.role is UserRole.MEMBER
    assert user.is_active is True
    assert database_session.in_transaction() is True


def test_user_repository_finds_user_by_id_and_normalized_email(
    database_session: Session,
) -> None:
    repository = SqlAlchemyUserRepository(database_session)
    created_user = repository.create(
        NewUser(
            email="lookup@example.com",
            password_hash="$argon2id$lookup-example",
        )
    )

    found_by_id = repository.get_by_id(created_user.user_id)
    found_by_email = repository.get_by_email(" LOOKUP@EXAMPLE.COM ")

    assert found_by_id == created_user
    assert found_by_email == created_user


def test_user_repository_returns_none_for_missing_user(
    database_session: Session,
) -> None:
    repository = SqlAlchemyUserRepository(database_session)

    assert repository.get_by_id(9_000_000_000) is None
    assert repository.get_by_email("missing@example.com") is None


def test_user_repository_translates_duplicate_email_conflict(
    database_session: Session,
) -> None:
    repository = SqlAlchemyUserRepository(database_session)

    repository.create(
        NewUser(
            email="duplicate@example.com",
            password_hash="$argon2id$first-example",
        )
    )

    with pytest.raises(UserRepositoryConflictError):
        repository.create(
            NewUser(
                email=" DUPLICATE@EXAMPLE.COM ",
                password_hash="$argon2id$second-example",
            )
        )


def test_user_repository_does_not_commit_created_user(
    database_session: Session,
    postgresql_test_engine: Engine,
) -> None:
    repository = SqlAlchemyUserRepository(database_session)

    user = repository.create(
        NewUser(
            email="uncommitted@example.com",
            password_hash="$argon2id$uncommitted-example",
        )
    )

    with postgresql_test_engine.connect() as connection:
        visible_user_id = connection.scalar(
            select(UserRecord.user_id).where(UserRecord.user_id == user.user_id)
        )

    assert visible_user_id is None


def test_sqlalchemy_user_repository_rejects_invalid_type(
    database_session: Session,
) -> None:
    repository = SqlAlchemyUserRepository(database_session)

    with pytest.raises(TypeError, match="NewUser"):
        repository.create("not-a-user")  # type: ignore[arg-type]
