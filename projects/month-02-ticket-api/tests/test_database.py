import asyncio
from contextlib import contextmanager
from unittest.mock import Mock, call

import pytest
from fastapi import FastAPI, Request
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

import ticket_api.lifespan as lifespan_module
from ticket_api.config import Settings
from ticket_api.database import (
    create_database_engine,
    create_session_factory,
)
from ticket_api.dependencies import get_session, get_session_factory


def test_create_database_engine_uses_postgresql_psycopg_driver() -> None:
    settings = Settings(
        database_url=(
            "postgresql+psycopg://example_user@localhost:5432/example_database"
        ),
        _env_file=None,
        jwt_secret="x" * 32,
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
        jwt_secret="x" * 32,
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


def test_get_session_commits_and_closes_after_success() -> None:
    session = Mock(spec=Session)
    session_factory = Mock(return_value=session)
    session_scope = contextmanager(get_session)

    with session_scope(session_factory) as provided_session:
        assert provided_session is session
        assert session.mock_calls == []

    session_factory.assert_called_once_with()
    assert session.mock_calls == [call.commit(), call.close()]


def test_get_session_rolls_back_and_closes_after_error() -> None:
    session = Mock(spec=Session)
    session_factory = Mock(return_value=session)
    session_scope = contextmanager(get_session)

    error = RuntimeError("Application error occurred")

    with pytest.raises(RuntimeError) as exc_info:
        with session_scope(session_factory):
            raise error

    assert exc_info.value is error
    session_factory.assert_called_once_with()
    assert session.mock_calls == [call.rollback(), call.close()]


def test_get_session_rolls_back_and_closes_after_commit_error() -> None:
    session = Mock(spec=Session)
    error = RuntimeError("Commit failed")
    session.commit.side_effect = error

    session_factory = Mock(return_value=session)
    session_scope = contextmanager(get_session)

    with pytest.raises(RuntimeError) as exc_info:
        with session_scope(session_factory):
            pass

    assert exc_info.value is error
    session_factory.assert_called_once_with()
    assert session.mock_calls == [call.commit(), call.rollback(), call.close()]


def test_database_lifespan_provides_factory_and_disposes_engine(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = FastAPI()
    settings = Mock(spec=Settings)
    engine = Mock(spec=Engine)
    session_factory = Mock(spec=sessionmaker)

    settings_provider = Mock(return_value=settings)
    engine_builder = Mock(return_value=engine)
    factory_builder = Mock(return_value=session_factory)

    monkeypatch.setattr(lifespan_module, "get_settings", settings_provider)
    monkeypatch.setattr(lifespan_module, "create_database_engine", engine_builder)
    monkeypatch.setattr(lifespan_module, "create_session_factory", factory_builder)

    request = Request({"type": "http", "app": app})

    async def exercise_lifespan() -> None:
        async with lifespan_module.database_lifespan(app):
            assert get_session_factory(request) is session_factory
            engine.dispose.assert_not_called()

    asyncio.run(exercise_lifespan())

    settings_provider.assert_called_once_with()
    engine_builder.assert_called_once_with(settings)
    factory_builder.assert_called_once_with(engine)
    engine.dispose.assert_called_once_with()


def test_database_lifespan_disposes_engine_on_context_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = FastAPI()
    settings = Mock(spec=Settings)
    engine = Mock(spec=Engine)
    session_factory = Mock(spec=sessionmaker)

    settings_provider = Mock(return_value=settings)
    engine_builder = Mock(return_value=engine)
    factory_builder = Mock(return_value=session_factory)

    monkeypatch.setattr(lifespan_module, "get_settings", settings_provider)
    monkeypatch.setattr(lifespan_module, "create_database_engine", engine_builder)
    monkeypatch.setattr(lifespan_module, "create_session_factory", factory_builder)

    error = RuntimeError("Context execution error")

    async def excercise_lifespan() -> None:
        async with lifespan_module.database_lifespan(app):
            raise error

    with pytest.raises(RuntimeError) as exc_info:
        asyncio.run(excercise_lifespan())

    assert exc_info.value is error
    engine.dispose.assert_called_once_with()


def test_database_lifespan_disposes_engine_when_factory_creation_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    app = FastAPI()
    settings = Mock(spec=Settings)
    engine = Mock(spec=Engine)

    settings_provider = Mock(return_value=settings)
    engine_builder = Mock(return_value=engine)
    factory_builder = Mock()

    error = RuntimeError("Factory creation error")
    factory_builder.side_effect = error

    monkeypatch.setattr(lifespan_module, "get_settings", settings_provider)
    monkeypatch.setattr(lifespan_module, "create_database_engine", engine_builder)
    monkeypatch.setattr(lifespan_module, "create_session_factory", factory_builder)

    async def exercise_lifespan() -> None:
        async with lifespan_module.database_lifespan(app):
            pytest.fail("Factory creation failed, but the lifespan body was entered")

    with pytest.raises(RuntimeError) as exc_info:
        asyncio.run(exercise_lifespan())

    assert exc_info.value is error
    engine.dispose.assert_called_once_with()
