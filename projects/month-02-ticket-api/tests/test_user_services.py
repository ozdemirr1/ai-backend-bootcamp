import pytest

from ticket_api.repositories import InMemoryUserRepository
from ticket_api.services import DuplicateUserError, RegistrationService
from ticket_api.user_models import UserRole


class RecordingPasswordHasher:
    def __init__(self) -> None:
        self.received_password: str | None = None

    def hash_password(self, plain_password: str) -> str:
        self.received_password = plain_password
        return "$argon2id$synthetic-test-hash"


def test_registration_service_creates_member_and_active_user() -> None:
    repository = InMemoryUserRepository()
    hasher = RecordingPasswordHasher()
    service = RegistrationService(repository, hasher)

    user = service.register_user("furkan@example.com", "my_secret_password")

    assert user.role is UserRole.MEMBER
    assert user.is_active is True


def test_registration_service_sends_plain_password_to_hasher() -> None:
    repository = InMemoryUserRepository()
    hasher = RecordingPasswordHasher()
    service = RegistrationService(repository, hasher)

    plain_password = "my_secret_password"
    service.register_user("furkan@example.com", plain_password)

    assert hasher.received_password == plain_password


def test_registration_service_stores_only_synthetic_hash() -> None:
    repository = InMemoryUserRepository()
    hasher = RecordingPasswordHasher()
    service = RegistrationService(repository, hasher)

    plain_password = "my_secret_password"
    created = service.register_user("furkan@example.com", plain_password)

    assert created.password_hash == "$argon2id$synthetic-test-hash"
    assert created.password_hash != plain_password


def test_registration_service_normalizes_email() -> None:
    repository = InMemoryUserRepository()
    hasher = RecordingPasswordHasher()
    service = RegistrationService(repository, hasher)

    user = service.register_user("  FURKAN@EXAMPLE.COM  ", "password123")

    assert user.email == "furkan@example.com"


def test_registration_service_raises_duplicate_error_on_second_registration() -> None:
    repository = InMemoryUserRepository()
    hasher = RecordingPasswordHasher()
    service = RegistrationService(repository, hasher)

    service.register_user("furkan@example.com", "password123")

    with pytest.raises(DuplicateUserError):
        service.register_user("FURKAN@example.com", "password456")


def test_registration_service_rejects_invalid_email_before_hashing() -> None:
    repository = InMemoryUserRepository()
    hasher = RecordingPasswordHasher()
    service = RegistrationService(repository, hasher)

    with pytest.raises(ValueError, match="email"):
        service.register_user("invalid-email", "password123")

    assert hasher.received_password is None
