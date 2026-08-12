from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, StringConstraints

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
    priority: Literal["low", "medium", "high", "critical"]
