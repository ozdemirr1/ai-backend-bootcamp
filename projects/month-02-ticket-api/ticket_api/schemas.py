from typing import Annotated, Literal, Self

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StringConstraints,
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
