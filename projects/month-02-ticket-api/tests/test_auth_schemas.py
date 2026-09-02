import pytest
from pydantic import ValidationError

from ticket_api.schemas import UserRegisterRequest, UserResponse


def test_user_register_request_normalizes_email() -> None:
    request = UserRegisterRequest(
        email="  Furkan@Example.COM  ",
        password="validpassword123",
    )

    assert request.email == "furkan@example.com"


def test_user_register_request_rejects_short_password() -> None:
    with pytest.raises(ValidationError):
        UserRegisterRequest(
            email="furkan@example.com",
            password="short",
        )


def test_user_register_request_rejects_blank_password() -> None:
    with pytest.raises(ValidationError, match="password cannot be blank"):
        UserRegisterRequest(
            email="furkan@example.com",
            password="                ",
        )


def test_user_register_request_rejects_extra_role_field() -> None:
    with pytest.raises(ValidationError):
        UserRegisterRequest(
            email="furkan@example.com",
            password="validpassword123",
            role="admin",
        )


def test_user_register_request_preserves_password() -> None:
    password_with_spaces = " valid password 123 "
    request = UserRegisterRequest(
        email="furkan@example.com",
        password=password_with_spaces,
    )

    assert request.password == password_with_spaces


def test_user_response_accepts_valid_user() -> None:
    response = UserResponse(
        user_id=1,
        email="furkan@example.com",
        role="member",
        is_active=True,
    )

    assert response.user_id == 1
    assert response.email == "furkan@example.com"
    assert response.role == "member"
    assert response.is_active is True


def test_user_response_rejects_password_hash() -> None:
    with pytest.raises(ValidationError):
        UserResponse(
            user_id=1,
            email="furkan@example.com",
            role="member",
            is_active=True,
            password_hash="$argon2id$example",
        )


def test_user_response_rejects_invalid_role() -> None:
    with pytest.raises(ValidationError):
        UserResponse(
            user_id=1,
            email="furkan@example.com",
            role="superadmin",
            is_active=True,
        )
