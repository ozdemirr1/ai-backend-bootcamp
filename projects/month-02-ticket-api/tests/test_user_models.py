import pytest

from ticket_api.user_models import NewUser, User, UserRole


def test_new_user_normalizes_email():
    user = NewUser(
        email="  Furkan@Example.COM  ",
        password_hash="$argon2id$example",
    )
    assert user.email == "furkan@example.com"


def test_new_user_rejects_invalid_email():
    with pytest.raises(ValueError, match="email must be valid"):
        NewUser(
            email="not-an-email",
            password_hash="$argon2id$example",
        )


def test_new_user_rejects_non_string_email():
    with pytest.raises(TypeError, match="email must be a str"):
        NewUser(
            email=123,
            password_hash="$argon2id$example",
        )


def test_new_user_rejects_empty_password_hash():
    with pytest.raises(ValueError, match="password_hash cannot be empty"):
        NewUser(
            email="furkan@example.com",
            password_hash="   ",
        )


def test_new_user_preserves_password_hash_exactly():
    hash_val = " $argon2id$example "
    user = NewUser(
        email="furkan@example.com",
        password_hash=hash_val,
    )
    assert user.password_hash == hash_val


def test_user_rejects_non_positive_id():
    with pytest.raises(ValueError, match="positive"):
        User(
            user_id=0,
            email="furkan@example.com",
            password_hash="$argon2id$example",
            role=UserRole.MEMBER,
            is_active=True,
        )


def test_user_rejects_raw_string_role():
    with pytest.raises(TypeError, match="role"):
        User(
            user_id=1,
            email="furkan@example.com",
            password_hash="$argon2id$example",
            role="member",
            is_active=True,
        )


def test_user_rejects_non_boolean_active_state():
    with pytest.raises(TypeError, match="is_active"):
        User(
            user_id=1,
            email="furkan@example.com",
            password_hash="$argon2id$example",
            role=UserRole.MEMBER,
            is_active=1,
        )


def test_user_accepts_member_role_and_active_state():
    user = User(
        user_id=1,
        email="furkan@example.com",
        password_hash="$argon2id$example",
        role=UserRole.MEMBER,
        is_active=False,
    )
    assert user.user_id == 1
    assert user.role is UserRole.MEMBER
    assert user.is_active is False
