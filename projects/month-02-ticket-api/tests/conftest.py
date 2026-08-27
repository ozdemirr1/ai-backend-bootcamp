import os
from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session

from ticket_api.config import get_settings
from ticket_api.persistence_models import TicketRecord

TEST_DATABASE_NAME = "opsdesk_test"


@pytest.fixture(scope="session")
def postgresql_test_engine() -> Iterator[Engine]:
    if os.getenv("RUN_DATABASE_TESTS") != "1":
        pytest.skip("set RUN_DATABASE_TESTS=1 to run PostgreSQL integration tests")

    database_url = make_url(get_settings().database_url.get_secret_value()).set(
        database=TEST_DATABASE_NAME
    )

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
    )

    try:
        with engine.connect() as connection:
            row = connection.execute(
                text(
                    """
                    SELECT
                        current_database() AS database_name,
                        current_user AS role_name,
                        r.rolsuper AS role_is_superuser,
                        to_regclass(
                            'public.tickets'
                        ) AS tickets_table
                    FROM pg_roles AS r
                    WHERE r.rolname = current_user
                    """
                )
            ).one()

            if row.database_name != TEST_DATABASE_NAME:
                raise RuntimeError("integration tests require opsdesk_test")

            if row.role_name == "postgres":
                raise RuntimeError("integration tests must not use a superuser")

            if row.tickets_table is None:
                raise RuntimeError("opsdesk_test must be migrated before testing")

            if row.role_is_superuser:
                raise RuntimeError(
                    f"integration tests must not use a superuser role: {row.role_name}"
                )

        yield engine
    finally:
        engine.dispose()


@pytest.fixture
def database_session(
    postgresql_test_engine: Engine,
) -> Iterator[Session]:
    with postgresql_test_engine.connect() as connection:
        transaction = connection.begin()

        existing_ticket_count = connection.scalar(
            select(func.count()).select_from(TicketRecord)
        )

        if existing_ticket_count != 0:
            transaction.rollback()
            raise RuntimeError("opsdesk_test.tickets must be empty before testing")

        session = Session(
            bind=connection,
            autoflush=False,
            expire_on_commit=False,
        )

        try:
            yield session
        finally:
            session.close()

            if transaction.is_active:
                transaction.rollback()
