from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from ticket_api.dependencies import get_current_user, get_ticket_service
from ticket_api.main import create_app
from ticket_api.models import Ticket, TicketPriority
from ticket_api.repositories import InMemoryTicketRepository
from ticket_api.services import TicketService
from ticket_api.user_models import User, UserRole

TEST_CURRENT_USER = User(
    user_id=7,
    email="ticket-owner@example.com",
    password_hash="$argon2id$synthetic-ticket-owner",
    role=UserRole.MEMBER,
    is_active=True,
)


@pytest.fixture
def client() -> Iterator[TestClient]:
    test_app = create_app(lifespan_handler=None)

    repository = InMemoryTicketRepository()
    service = TicketService(repository)

    def get_test_ticket_service() -> TicketService:
        return service

    def get_test_current_user() -> User:
        return TEST_CURRENT_USER

    test_app.dependency_overrides[get_ticket_service] = get_test_ticket_service
    test_app.dependency_overrides[get_current_user] = get_test_current_user

    try:
        with TestClient(test_app) as test_client:
            yield test_client
    finally:
        test_app.dependency_overrides.pop(get_ticket_service, None)
        test_app.dependency_overrides.pop(get_current_user, None)


def test_read_health(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["content-type"] == "application/json"


def test_list_tickets_returns_empty_list(client: TestClient) -> None:
    response = client.get("/tickets")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tickets_accepts_query_parameters(client: TestClient) -> None:
    client.post(
        "/tickets",
        json={
            "title": "VPN connection fails",
            "priority": "high",
        },
    )

    response = client.get(
        "/tickets",
        params={
            "status": "open",
            "limit": 5,
        },
    )

    assert response.status_code == 200
    assert response.json() == [
        {
            "ticket_id": 1,
            "title": "VPN connection fails",
            "priority": "high",
            "status": "open",
        }
    ]


def test_list_tickets_respects_limit(client: TestClient) -> None:
    client.post("/tickets", json={"title": "VPN connection fails", "priority": "high"})
    client.post("/tickets", json={"title": "Email is down", "priority": "medium"})

    response = client.get(
        "/tickets",
        params={"limit": 1},
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["ticket_id"] == 1


def test_list_tickets_rejects_invalid_status(client: TestClient) -> None:
    response = client.get(
        "/tickets",
        params={"status": "unknown"},
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["query", "status"]
    assert error["type"] == "literal_error"


def test_read_ticket_returns_existing_ticket(client: TestClient) -> None:
    create_response = client.post(
        "/tickets",
        json={
            "title": "VPN connection fails",
            "priority": "high",
        },
    )

    assert create_response.status_code == 201

    ticket_id = create_response.json()["ticket_id"]

    response = client.get(f"/tickets/{ticket_id}")

    assert response.status_code == 200
    assert response.json() == {
        "ticket_id": 1,
        "title": "VPN connection fails",
        "priority": "high",
        "status": "open",
    }


def test_read_ticket_returns_404_when_ticket_is_missing(client: TestClient) -> None:
    response = client.get("/tickets/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Ticket 999 not found",
    }
    assert response.headers["content-type"] == "application/json"


def test_read_ticket_rejects_non_integer_id(client: TestClient) -> None:
    response = client.get("/tickets/not-a-number")

    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["path", "ticket_id"]
    assert error["type"] == "int_parsing"


def test_list_tickets_rejects_non_integer_limit(client: TestClient) -> None:
    response = client.get("/tickets?limit=not-a-number")

    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["query", "limit"]
    assert error["type"] == "int_parsing"


def test_preview_ticket_accepts_valid_body(client: TestClient) -> None:
    response = client.post(
        "/tickets/preview",
        json={
            "title": "VPN connection fails",
            "priority": "high",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "title": "VPN connection fails",
        "priority": "high",
    }


def test_preview_ticket_strips_title_whitespace(client: TestClient) -> None:
    response = client.post(
        "/tickets/preview",
        json={
            "title": "  VPN connection fails  ",
            "priority": "high",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "title": "VPN connection fails",
        "priority": "high",
    }


def test_preview_ticket_rejects_missing_title(client: TestClient) -> None:
    response = client.post(
        "/tickets/preview",
        json={"priority": "high"},
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "title"]
    assert error["type"] == "missing"


def test_preview_ticket_rejects_whitespace_only_title(client: TestClient) -> None:
    response = client.post(
        "/tickets/preview",
        json={
            "title": "   ",
            "priority": "high",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "title"]
    assert error["type"] == "string_too_short"


def test_preview_ticket_rejects_title_over_maximum_length(client: TestClient) -> None:
    response = client.post(
        "/tickets/preview",
        json={
            "title": "A" * 101,
            "priority": "high",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "title"]
    assert error["type"] == "string_too_long"


def test_preview_ticket_rejects_invalid_priority(client: TestClient) -> None:
    response = client.post(
        "/tickets/preview",
        json={
            "title": "VPN connection fails",
            "priority": "urgent",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "priority"]
    assert error["type"] == "literal_error"


def test_preview_ticket_rejects_non_string_title(client: TestClient) -> None:
    response = client.post(
        "/tickets/preview",
        json={
            "title": 123,
            "priority": "high",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "title"]
    assert error["type"] == "string_type"


def test_preview_ticket_rejects_extra_fields(client: TestClient) -> None:
    response = client.post(
        "/tickets/preview",
        json={
            "title": "VPN connection fails",
            "priority": "high",
            "status": "closed",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "status"]
    assert error["type"] == "extra_forbidden"


def test_preview_ticket_rejects_missing_priority(client: TestClient) -> None:
    response = client.post(
        "/tickets/preview",
        json={"title": "VPN connection fails"},
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "priority"]
    assert error["type"] == "missing"


def test_create_ticket_returns_created_ticket(client: TestClient) -> None:
    response = client.post(
        "/tickets",
        json={
            "title": "VPN connection fails",
            "priority": "high",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "ticket_id": 1,
        "title": "VPN connection fails",
        "priority": "high",
        "status": "open",
    }
    assert response.headers["content-type"] == "application/json"


def test_create_ticket_assigns_sequential_ids(client: TestClient) -> None:
    first_response = client.post(
        "/tickets",
        json={
            "title": "VPN connection fails",
            "priority": "high",
        },
    )

    second_response = client.post(
        "/tickets",
        json={
            "title": "Email is down",
            "priority": "medium",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 201
    assert first_response.json()["ticket_id"] == 1
    assert second_response.json()["ticket_id"] == 2


def test_update_ticket_changes_only_provided_field(
    client: TestClient,
) -> None:
    create_response = client.post(
        "/tickets",
        json={
            "title": "VPN connection fails",
            "priority": "high",
        },
    )

    ticket_id = create_response.json()["ticket_id"]

    response = client.patch(
        f"/tickets/{ticket_id}",
        json={
            "title": "  Updated VPN issue  ",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "ticket_id": 1,
        "title": "Updated VPN issue",
        "priority": "high",
        "status": "open",
    }

    read_response = client.get(f"/tickets/{ticket_id}")
    assert read_response.json() == response.json()


def test_update_ticket_changes_multiple_fields(
    client: TestClient,
) -> None:
    create_response = client.post(
        "/tickets",
        json={
            "title": "VPN connection fails",
            "priority": "high",
        },
    )

    ticket_id = create_response.json()["ticket_id"]

    response = client.patch(
        f"/tickets/{ticket_id}",
        json={
            "priority": "critical",
            "status": "in_progress",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "ticket_id": 1,
        "title": "VPN connection fails",
        "priority": "critical",
        "status": "in_progress",
    }


def test_update_ticket_returns_404_when_ticket_is_missing(
    client: TestClient,
) -> None:
    response = client.patch(
        "/tickets/999",
        json={
            "status": "resolved",
        },
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Ticket 999 not found",
    }


def test_update_ticket_rejects_empty_body(
    client: TestClient,
) -> None:
    response = client.patch(
        "/tickets/1",
        json={},
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["body"]
    assert error["type"] == "value_error"


def test_update_ticket_rejects_invalid_status(
    client: TestClient,
) -> None:
    response = client.patch(
        "/tickets/1",
        json={
            "status": "waiting",
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "status"]
    assert error["type"] == "literal_error"


def test_delete_ticket_returns_204_and_removes_ticket(
    client: TestClient,
) -> None:
    create_response = client.post(
        "/tickets",
        json={
            "title": "VPN connection fails",
            "priority": "high",
        },
    )

    ticket_id = create_response.json()["ticket_id"]

    delete_response = client.delete(
        f"/tickets/{ticket_id}",
    )

    assert delete_response.status_code == 204
    assert delete_response.content == b""

    read_response = client.get(
        f"/tickets/{ticket_id}",
    )

    assert read_response.status_code == 404
    assert read_response.json() == {
        "detail": f"Ticket {ticket_id} not found",
    }


def test_delete_ticket_returns_404_when_ticket_is_missing(
    client: TestClient,
) -> None:
    response = client.delete("/tickets/999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Ticket 999 not found",
    }


def test_delete_ticket_rejects_non_integer_id(
    client: TestClient,
) -> None:
    response = client.delete(
        "/tickets/not-a-number",
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["path", "ticket_id"]
    assert error["type"] == "int_parsing"


def test_create_ticket_returns_409_for_duplicate_id(
    client: TestClient,
) -> None:
    existing_ticket = Ticket(
        ticket_id=1,
        title="Existing ticket",
        priority=TicketPriority.LOW,
    )

    repository = InMemoryTicketRepository()
    repository.add(existing_ticket)

    conflicting_service = TicketService(repository)

    def get_conflicting_ticket_service() -> TicketService:
        return conflicting_service

    client.app.dependency_overrides[get_ticket_service] = get_conflicting_ticket_service

    response = client.post(
        "/tickets",
        json={
            "title": "New ticket",
            "priority": "high",
        },
    )

    assert response.status_code == 409
    assert response.json() == {
        "detail": "Ticket 1 already exists",
    }
    assert response.headers["content-type"] == "application/json"

    read_response = client.get("/tickets/1")

    assert read_response.status_code == 200
    assert read_response.json() == {
        "ticket_id": 1,
        "title": "Existing ticket",
        "priority": "low",
        "status": "open",
    }


def test_list_tickets_rejects_limit_below_minimum(
    client: TestClient,
) -> None:
    response = client.get(
        "/tickets",
        params={"limit": 0},
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["query", "limit"]
    assert error["type"] == "greater_than_equal"


def test_list_tickets_rejects_limit_above_maximum(
    client: TestClient,
) -> None:
    response = client.get(
        "/tickets",
        params={"limit": 101},
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["query", "limit"]
    assert error["type"] == "less_than_equal"


def test_create_ticket_derives_owner_from_current_user(
    client: TestClient,
) -> None:
    response = client.post(
        "/tickets",
        json={
            "title": "Owned ticket",
            "priority": "high",
        },
    )

    assert response.status_code == 201

    ticket_id = response.json()["ticket_id"]

    service_provider = client.app.dependency_overrides[get_ticket_service]
    stored_ticket = service_provider().get_ticket(ticket_id)

    assert stored_ticket.owner_id == TEST_CURRENT_USER.user_id


def test_create_ticket_rejects_client_supplied_owner_id(
    client: TestClient,
) -> None:
    response = client.post(
        "/tickets",
        json={
            "title": "Ownership escalation attempt",
            "priority": "high",
            "owner_id": 999,
        },
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "owner_id"]
    assert error["type"] == "extra_forbidden"
