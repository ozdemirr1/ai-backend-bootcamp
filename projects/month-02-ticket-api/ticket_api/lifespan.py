from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from ticket_api.config import get_settings
from ticket_api.database import create_database_engine, create_session_factory


@asynccontextmanager
async def database_lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_settings()
    engine = create_database_engine(settings)

    try:
        app.state.session_factory = create_session_factory(engine)
        yield
    finally:
        engine.dispose()
