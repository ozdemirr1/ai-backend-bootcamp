import os
from collections.abc import Iterator

import pytest
from sqlalchemy import create_engine, func, select, text
from sqlalchemy.engine import Engine, make_url
from sqlalchemy.orm import Session

from ticket_api.config import Settings
from ticket_api.persistence_models import TicketRecord, UserRecord

TEST_DATABASE_NAME = "opsdesk_test"
TEST_JWT_SECRET = "integration-test-jwt-secret-with-32-characters"


@pytest.fixture(scope="session")
def postgresql_test_engine() -> Iterator[Engine]:
    if os.getenv("RUN_DATABASE_TESTS") != "1":
        pytest.skip("set RUN_DATABASE_TESTS=1 to run PostgreSQL integration tests")

    settings = Settings(jwt_secret=TEST_JWT_SECRET)
    database_url = make_url(settings.database_url.get_secret_value()).set(
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
                        to_regclass('public.tickets') AS tickets_table,
                        to_regclass('public.users') AS users_table,
                        EXISTS (
                            SELECT 1
                            FROM information_schema.columns
                            WHERE table_schema = 'public'
                            AND table_name = 'tickets'
                            AND column_name = 'owner_id'
                        ) AS owner_id_exists
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

            if row.users_table is None:
                raise RuntimeError("opsdesk_test must contain the users table")

            if not row.owner_id_exists:
                raise RuntimeError("opsdesk_test.tickets must contain owner_id")

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

        existing_user_count = connection.scalar(
            select(func.count()).select_from(UserRecord)
        )

        if existing_ticket_count != 0:
            transaction.rollback()
            raise RuntimeError("opsdesk_test.tickets must be empty before testing")

        if existing_user_count != 0:
            transaction.rollback()
            raise RuntimeError("opsdesk_test.users must be empty before testing")
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


@pytest.fixture
def synthetic_auth_settings() -> Settings:
    return Settings(
        database_url="postgresql+psycopg://unused",
        jwt_secret=TEST_JWT_SECRET,
        access_token_expire_minutes=30,
        _env_file=None,
    )
