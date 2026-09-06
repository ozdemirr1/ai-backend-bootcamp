import pytest

from ticket_api.passwords import (
    PasswordHasher,
    get_dummy_password_hash,
)


@pytest.fixture
def hasher() -> PasswordHasher:
    return PasswordHasher()


def test_hash_is_not_equal_to_plain_password(hasher: PasswordHasher) -> None:
    plain_password = "secure_password_123"
    hashed = hasher.hash_password(plain_password)

    assert hashed != plain_password


def test_correct_password_verifies_successfully(hasher: PasswordHasher) -> None:
    plain_password = "secure_password_123"
    hashed = hasher.hash_password(plain_password)

    assert hasher.verify_password(plain_password, hashed) is True


def test_incorrect_password_fails_verification(hasher: PasswordHasher) -> None:
    plain_password = "secure_password_123"
    hashed = hasher.hash_password(plain_password)

    assert hasher.verify_password("wrong_password_456", hashed) is False


def test_same_password_generates_different_hashes_but_both_verify(
    hasher: PasswordHasher,
) -> None:
    plain_password = "secure_password_123"

    hash1 = hasher.hash_password(plain_password)
    hash2 = hasher.hash_password(plain_password)

    assert hash1 != hash2

    # Ancak ikisi de aynı düz parola ile doğrulanabilmeli
    assert hasher.verify_password(plain_password, hash1) is True
    assert hasher.verify_password(plain_password, hash2) is True


def test_generated_hash_starts_with_argon2id(hasher: PasswordHasher) -> None:
    plain_password = "secure_password_123"
    hashed = hasher.hash_password(plain_password)

    assert hashed.startswith("$argon2id$")


def test_dummy_password_hash_is_valid_argon2id_and_cached() -> None:
    get_dummy_password_hash.cache_clear()

    first_hash = get_dummy_password_hash()
    second_hash = get_dummy_password_hash()

    assert first_hash.startswith("$argon2id$")
    assert second_hash == first_hash
