from collections.abc import Iterator
from datetime import timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session, sessionmaker

from ticket_api.clock import SystemClock
from ticket_api.config import Settings, get_settings
from ticket_api.passwords import (
    PasswordHasher,
    get_dummy_password_hash,
)
from ticket_api.services import (
    AuthenticationService,
    CurrentUserService,
    InvalidAuthenticationError,
    RegistrationService,
    TicketService,
)
from ticket_api.sqlalchemy_repositories import (
    SqlAlchemyTicketRepository,
    SqlAlchemyUserRepository,
)
from ticket_api.tokens import (
    InvalidAccessTokenError,
    JwtAccessTokenManager,
)
from ticket_api.user_models import User


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


SettingsDependency = Annotated[
    Settings,
    Depends(get_settings),
]


def get_access_token_manager(
    settings: SettingsDependency,
) -> JwtAccessTokenManager:
    return JwtAccessTokenManager(
        secret=settings.jwt_secret.get_secret_value(),
        lifetime=timedelta(minutes=settings.access_token_expire_minutes),
        clock=SystemClock(),
    )


AccessTokenManagerDependency = Annotated[
    JwtAccessTokenManager,
    Depends(get_access_token_manager),
]


def get_authentication_service(
    session: SessionDependency,
    token_manager: AccessTokenManagerDependency,
) -> AuthenticationService:
    repository = SqlAlchemyUserRepository(session)
    password_verifier = PasswordHasher()

    return AuthenticationService(
        repository=repository,
        password_verifier=password_verifier,
        token_issuer=token_manager,
        dummy_password_hash=get_dummy_password_hash(),
    )


def get_current_user_service(
    session: SessionDependency,
    token_manager: AccessTokenManagerDependency,
) -> CurrentUserService:
    repository = SqlAlchemyUserRepository(session)

    return CurrentUserService(
        repository=repository,
        token_decoder=token_manager,
    )


CurrentUserServiceDependency = Annotated[
    CurrentUserService,
    Depends(get_current_user_service),
]


bearer_scheme = HTTPBearer(
    bearerFormat="JWT",
    auto_error=False,
)


BearerCredentialsDependency = Annotated[
    HTTPAuthorizationCredentials | None,
    Depends(bearer_scheme),
]


def _invalid_authentication_error() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )


def get_current_user(
    credentials: BearerCredentialsDependency,
    service: CurrentUserServiceDependency,
) -> User:
    if credentials is None or credentials.scheme.casefold() != "bearer":
        raise _invalid_authentication_error()

    try:
        return service.get_current_user(credentials.credentials)
    except (
        InvalidAccessTokenError,
        InvalidAuthenticationError,
    ) as exc:
        raise _invalid_authentication_error() from exc


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
