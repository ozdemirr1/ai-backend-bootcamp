from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

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
