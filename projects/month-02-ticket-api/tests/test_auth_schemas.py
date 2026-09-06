import pytest
from pydantic import ValidationError

from ticket_api.schemas import (
    AccessTokenResponse,
    UserLoginRequest,
    UserRegisterRequest,
    UserResponse,
)


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


def test_user_login_request_normalizes_email() -> None:
    request = UserLoginRequest(email=" FURKAN@Example.COM ", password="password123")
    assert request.email == "furkan@example.com"


def test_user_login_request_rejects_empty_password() -> None:
    with pytest.raises(ValidationError):
        UserLoginRequest(email="furkan@example.com", password="")


def test_user_login_request_preserves_password() -> None:
    password_with_spaces = "  my password 123  "
    request = UserLoginRequest(
        email="furkan@example.com", password=password_with_spaces
    )
    assert request.password == password_with_spaces


def test_user_login_request_rejects_invalid_email() -> None:
    with pytest.raises(ValidationError):
        UserLoginRequest(email="not-an-email", password="password123")


def test_user_login_request_rejects_extra_role_field() -> None:
    with pytest.raises(ValidationError):
        UserLoginRequest(
            email="furkan@example.com",
            password="password123",
            role="admin",  # extra field
        )


def test_access_token_response_accepts_valid_token() -> None:
    response = AccessTokenResponse(
        access_token="eyJhbGciOiJIUzI1NiIsInR5cCI...", token_type="bearer"
    )
    assert response.access_token == "eyJhbGciOiJIUzI1NiIsInR5cCI..."
    assert response.token_type == "bearer"


def test_access_token_response_rejects_invalid_token_type() -> None:
    with pytest.raises(ValidationError):
        AccessTokenResponse(
            access_token="eyJhbGciOi...",
            token_type="basic",  # type: ignore[arg-type]
        )


def test_access_token_response_rejects_empty_access_token() -> None:
    with pytest.raises(ValidationError):
        AccessTokenResponse(access_token="", token_type="bearer")


def test_access_token_response_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        AccessTokenResponse(
            access_token="eyJhbGciOi...",
            token_type="bearer",
            expires_in=3600,  # extra field
        )
