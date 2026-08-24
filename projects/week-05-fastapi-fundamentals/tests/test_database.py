from ticket_api.config import Settings
from ticket_api.database import (
    create_database_engine,
    create_session_factory,
)


def test_create_database_engine_uses_postgresql_psycopg_driver() -> None:
    settings = Settings(
        database_url=(
            "postgresql+psycopg://example_user@localhost:5432/example_database"
        ),
        _env_file=None,
    )

    engine = create_database_engine(settings)

    try:
        assert engine.dialect.name == "postgresql"
        assert engine.dialect.driver == "psycopg"
        assert engine.url.host == "localhost"
        assert engine.url.port == 5432
        assert engine.url.database == "example_database"
    finally:
        engine.dispose()


def test_create_session_factory_uses_expected_engine_and_options() -> None:
    settings = Settings(
        database_url=(
            "postgresql+psycopg://example_user@localhost:5432/example_database"
        ),
        _env_file=None,
    )
    engine = create_database_engine(settings)
    session_factory = create_session_factory(engine)
    session = session_factory()

    try:
        assert session.get_bind() is engine
        assert session.autoflush is False
        assert session.expire_on_commit is False
    finally:
        session.close()
        engine.dispose()
