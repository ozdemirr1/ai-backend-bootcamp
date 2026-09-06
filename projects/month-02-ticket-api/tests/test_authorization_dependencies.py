import pytest
from fastapi import HTTPException

from ticket_api.dependencies import require_admin_user
from ticket_api.user_models import User, UserRole


def test_require_admin_user_returns_admin_user() -> None:
    admin_user = User(
        user_id=1,
        email="admin@example.com",
        password_hash="$argon2id$synthetic-test-hash",
        role=UserRole.ADMIN,
        is_active=True,
    )

    result = require_admin_user(admin_user)

    assert result is admin_user


def test_require_admin_user_rejects_member_user() -> None:
    member_user = User(
        user_id=2,
        email="member@example.com",
        password_hash="$argon2id$synthetic-test-hash",
        role=UserRole.MEMBER,
        is_active=True,
    )

    with pytest.raises(HTTPException) as exc_info:
        require_admin_user(member_user)

    assert exc_info.value.status_code == 403
    assert exc_info.value.detail == "Admin role required"
