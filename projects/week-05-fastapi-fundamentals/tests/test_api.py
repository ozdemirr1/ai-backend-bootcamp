from fastapi.testclient import TestClient

from ticket_api.main import app

client = TestClient(app)


def test_read_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["content-type"] == "application/json"


def test_list_tickets_uses_default_query_values() -> None:
    response = client.get("/tickets")

    assert response.status_code == 200
    assert response.json() == {"status_filter": None, "limit": 10}


def test_list_tickets_accepts_query_parameters() -> None:
    response = client.get(
        "/tickets",
        params={"status": "open", "limit": 5},
    )

    assert response.status_code == 200
    assert response.json() == {"status_filter": "open", "limit": 5}


def test_read_ticket_accepts_integer_id() -> None:
    response = client.get("/tickets/42")

    assert response.status_code == 200
    assert response.json() == {"ticket_id": 42}


def test_read_ticket_rejects_non_integer_id() -> None:
    response = client.get("/tickets/not-a-number")

    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["path", "ticket_id"]
    assert error["type"] == "int_parsing"


def test_list_tickets_rejects_non_integer_limit() -> None:
    response = client.get("/tickets?limit=not-a-number")

    assert response.status_code == 422
    error = response.json()["detail"][0]
    assert error["loc"] == ["query", "limit"]
    assert error["type"] == "int_parsing"


def test_preview_ticket_accepts_valid_body() -> None:
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


def test_preview_ticket_strips_title_whitespace() -> None:
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


def test_preview_ticket_rejects_missing_title() -> None:
    response = client.post(
        "/tickets/preview",
        json={"priority": "high"},
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "title"]
    assert error["type"] == "missing"


def test_preview_ticket_rejects_whitespace_only_title() -> None:
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


def test_preview_ticket_rejects_title_over_maximum_length() -> None:
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


def test_preview_ticket_rejects_invalid_priority() -> None:
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


def test_preview_ticket_rejects_non_string_title() -> None:
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


def test_preview_ticket_rejects_extra_fields() -> None:
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


def test_preview_ticket_rejects_missing_priority() -> None:
    response = client.post(
        "/tickets/preview",
        json={"title": "VPN connection fails"},
    )

    assert response.status_code == 422

    error = response.json()["detail"][0]
    assert error["loc"] == ["body", "priority"]
    assert error["type"] == "missing"
