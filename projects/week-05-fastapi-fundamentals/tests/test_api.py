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
