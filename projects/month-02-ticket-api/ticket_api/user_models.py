from dataclasses import dataclass
from enum import Enum

from email_validator import EmailNotValidError, validate_email


class UserRole(str, Enum):
    MEMBER = "member"
    ADMIN = "admin"


def normalize_user_email(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("email must be a str")

    try:
        validated = validate_email(
            value.strip(),
            check_deliverability=False,
        )
    except EmailNotValidError as exc:
        raise ValueError("email must be valid") from exc

    return validated.normalized.casefold()


def _validate_password_hash(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("password_hash must be a str")

    if not value or not value.strip():
        raise ValueError("password_hash cannot be empty or just whitespace")

    return value


@dataclass(frozen=True)
class NewUser:
    email: str
    password_hash: str

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "email",
            normalize_user_email(self.email),
        )
        object.__setattr__(
            self,
            "password_hash",
            _validate_password_hash(self.password_hash),
        )


@dataclass
class User:
    user_id: int
    email: str
    password_hash: str
    role: UserRole
    is_active: bool

    def __post_init__(self) -> None:
        if type(self.user_id) is not int:
            raise TypeError("user_id must be an int")
        if self.user_id <= 0:
            raise ValueError("user_id must be positive")

        self.email = normalize_user_email(self.email)
        self.password_hash = _validate_password_hash(self.password_hash)

        if type(self.role) is not UserRole:
            raise TypeError("role must be a UserRole instance")

        if type(self.is_active) is not bool:
            raise TypeError("is_active must be a strict bool")
