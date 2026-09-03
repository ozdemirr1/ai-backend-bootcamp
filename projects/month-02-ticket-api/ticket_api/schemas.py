from typing import Annotated, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
    field_validator,
    model_validator,
)

TicketPriority = Literal["low", "medium", "high", "critical"]
TicketStatus = Literal["open", "in_progress", "resolved", "closed"]

TicketTitle = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=3,
        max_length=100,
    ),
]


class TicketCreateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: TicketTitle
    priority: TicketPriority


class TicketResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    ticket_id: int = Field(gt=0)
    title: TicketTitle
    priority: TicketPriority
    status: TicketStatus


class TicketUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: TicketTitle | None = None
    priority: TicketPriority | None = None
    status: TicketStatus | None = None

    @model_validator(mode="after")
    def require_at_least_one_field(self) -> Self:
        if self.title is None and self.priority is None and self.status is None:
            raise ValueError("at least one field must be provided")

        return self


UserRole = Literal["member", "admin"]


class UserRegisterRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str = Field(
        strict=True,
        min_length=12,
        max_length=128,
    )

    @field_validator("email", mode="after")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).casefold()

    @field_validator("password")
    @classmethod
    def reject_blank_password(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("password cannot be blank")
        return value


class UserResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    user_id: int = Field(gt=0)
    email: EmailStr
    role: UserRole
    is_active: bool


class UserLoginRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    email: EmailStr
    password: str = Field(
        strict=True,
        min_length=1,
        max_length=128,
    )

    @field_validator("email", mode="after")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).casefold()


class AccessTokenResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    access_token: str = Field(min_length=1)
    token_type: Literal["bearer"] = "bearer"
