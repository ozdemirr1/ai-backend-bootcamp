from fastapi.testclient import TestClient

from ticket_api.main import app

client = TestClient(app)


def test_read_health() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert response.headers["content-type"] == "application/json"
