import pytest

from ticket_api.repositories import InMemoryUserRepository
from ticket_api.services import AuthenticationService, InvalidCredentialsError
from ticket_api.user_models import NewUser

DUMMY_PASSWORD_HASH = "$argon2id$synthetic-dummy-hash"


class RecordingPasswordVerifier:
    def __init__(self, result: bool) -> None:
        self.result = result
        self.calls: list[tuple[str, str]] = []

    def verify_password(
        self,
        plain_password: str,
        password_hash: str,
    ) -> bool:
        self.calls.append((plain_password, password_hash))
        return self.result


class RecordingTokenIssuer:
    def __init__(self) -> None:
        self.received_user_id: int | None = None

    def create_access_token(self, user_id: int) -> str:
        self.received_user_id = user_id
        return "synthetic.access.token"


def test_login_user_returns_token_on_success() -> None:
    repository = InMemoryUserRepository()
    user = repository.create(
        NewUser(email="furkan@example.com", password_hash="real-hash")
    )

    verifier = RecordingPasswordVerifier(result=True)
    issuer = RecordingTokenIssuer()
    service = AuthenticationService(repository, verifier, issuer, DUMMY_PASSWORD_HASH)

    token = service.login_user("furkan@example.com", "correct_password")

    assert token == "synthetic.access.token"
    assert issuer.received_user_id == user.user_id
    assert verifier.calls == [("correct_password", "real-hash")]


def test_login_user_rejects_wrong_password() -> None:
    repository = InMemoryUserRepository()
    repository.create(NewUser(email="furkan@example.com", password_hash="real-hash"))

    verifier = RecordingPasswordVerifier(result=False)
    issuer = RecordingTokenIssuer()
    service = AuthenticationService(repository, verifier, issuer, DUMMY_PASSWORD_HASH)

    with pytest.raises(InvalidCredentialsError, match="Invalid email or password"):
        service.login_user("furkan@example.com", "wrong_password")

    assert issuer.received_user_id is None
    assert verifier.calls == [("wrong_password", "real-hash")]


def test_login_user_rejects_missing_user_and_verifies_dummy_hash() -> None:
    repository = InMemoryUserRepository()

    verifier = RecordingPasswordVerifier(result=True)
    issuer = RecordingTokenIssuer()
    service = AuthenticationService(repository, verifier, issuer, DUMMY_PASSWORD_HASH)

    with pytest.raises(InvalidCredentialsError, match="Invalid email or password"):
        service.login_user("missing@example.com", "any_password")

    assert issuer.received_user_id is None
    assert verifier.calls == [("any_password", DUMMY_PASSWORD_HASH)]


def test_login_user_rejects_inactive_user() -> None:
    repository = InMemoryUserRepository()
    user = repository.create(
        NewUser(email="furkan@example.com", password_hash="real-hash")
    )

    user.is_active = False

    verifier = RecordingPasswordVerifier(result=True)
    issuer = RecordingTokenIssuer()
    service = AuthenticationService(repository, verifier, issuer, DUMMY_PASSWORD_HASH)

    with pytest.raises(InvalidCredentialsError, match="Invalid email or password"):
        service.login_user("furkan@example.com", "correct_password")

    assert issuer.received_user_id is None
    assert verifier.calls == [("correct_password", "real-hash")]
