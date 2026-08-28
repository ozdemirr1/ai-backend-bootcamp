from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import delete, func, select
from sqlalchemy.engine import Engine

from ticket_api.database import create_session_factory
from ticket_api.main import create_app
from ticket_api.persistence_models import TicketRecord

pytestmark = pytest.mark.integration


def test_create_ticket_commits_before_response(
    postgresql_test_engine: Engine,
) -> None:
    with postgresql_test_engine.connect() as connection:
        ticket_count = connection.scalar(select(func.count()).select_from(TicketRecord))

    assert ticket_count == 0

    test_app = create_app(lifespan_handler=None)
    test_app.state.session_factory = create_session_factory(postgresql_test_engine)

    title = f"API commit probe {uuid4().hex}"

    try:
        with TestClient(test_app) as client:
            response = client.post(
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

            get_response = client.get(f"/tickets/{ticket_id}")
            assert get_response.status_code == 200
            assert get_response.json() == data

    finally:
        with postgresql_test_engine.begin() as connection:
            connection.execute(delete(TicketRecord).where(TicketRecord.title == title))
