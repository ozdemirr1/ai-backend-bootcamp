import pytest

from ticket_api.repositories import InMemoryUserRepository
from ticket_api.services import (
    CurrentUserService,
    InvalidAuthenticationError,
)
from ticket_api.user_models import NewUser


class RecordingTokenDecoder:
    def __init__(self, user_id: int) -> None:
        self.user_id = user_id
        self.received_token: str | None = None

    def decode_access_token(self, token: str) -> int:
        self.received_token = token
        return self.user_id


def test_current_user_service_returns_active_user() -> None:
    repository = InMemoryUserRepository()
    user = repository.create(
        NewUser(
            email="furkan@example.com",
            password_hash="$argon2id$synthetic-hash",
        )
    )
    decoder = RecordingTokenDecoder(user.user_id)
    service = CurrentUserService(repository, decoder)

    result = service.get_current_user("synthetic.access.token")

    assert result == user
    assert decoder.received_token == "synthetic.access.token"


def test_current_user_service_rejects_missing_user() -> None:
    repository = InMemoryUserRepository()
    decoder = RecordingTokenDecoder(user_id=999)
    service = CurrentUserService(repository, decoder)

    with pytest.raises(
        InvalidAuthenticationError,
        match="Invalid authentication credentials",
    ):
        service.get_current_user("synthetic.access.token")


def test_current_user_service_rejects_inactive_user() -> None:
    repository = InMemoryUserRepository()
    user = repository.create(
        NewUser(
            email="furkan@example.com",
            password_hash="$argon2id$synthetic-hash",
        )
    )
    user.is_active = False

    decoder = RecordingTokenDecoder(user.user_id)
    service = CurrentUserService(repository, decoder)

    with pytest.raises(
        InvalidAuthenticationError,
        match="Invalid authentication credentials",
    ):
        service.get_current_user("synthetic.access.token")
