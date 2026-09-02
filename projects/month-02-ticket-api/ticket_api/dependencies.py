from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.orm import Session, sessionmaker

from ticket_api.passwords import PasswordHasher
from ticket_api.services import RegistrationService, TicketService
from ticket_api.sqlalchemy_repositories import (
    SqlAlchemyTicketRepository,
    SqlAlchemyUserRepository,
)


def get_session_factory(request: Request) -> sessionmaker[Session]:
    return request.app.state.session_factory


SessionFactoryDependency = Annotated[
    sessionmaker[Session], Depends(get_session_factory)
]


def get_session(
    session_factory: SessionFactoryDependency,
) -> Iterator[Session]:
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


SessionDependency = Annotated[
    Session,
    Depends(get_session, scope="function"),
]


def get_ticket_service(session: SessionDependency) -> TicketService:
    repository = SqlAlchemyTicketRepository(session)
    return TicketService(repository)


def get_registration_service(
    session: SessionDependency,
) -> RegistrationService:
    repository = SqlAlchemyUserRepository(session)
    password_hasher = PasswordHasher()

    return RegistrationService(
        repository=repository,
        password_hasher=password_hasher,
    )
