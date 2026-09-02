from dataclasses import dataclass
from enum import Enum


class TicketPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TicketStatus(str, Enum):
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"
    CLOSED = "closed"


def _normalize_ticket_title(value: str) -> str:
    if not isinstance(value, str):
        raise TypeError("title must be a str")

    normalized = value.strip()

    if len(normalized) < 3:
        raise ValueError("title must be at least 3 characters")

    if len(normalized) > 100:
        raise ValueError("title must be at most 100 characters")

    return normalized


@dataclass(frozen=True)
class NewTicket:
    title: str
    priority: TicketPriority

    def __post_init__(self) -> None:
        if not isinstance(self.priority, TicketPriority):
            raise TypeError("priority must be a TicketPriority instance")

        object.__setattr__(
            self,
            "title",
            _normalize_ticket_title(self.title),
        )


@dataclass
class Ticket:
    ticket_id: int
    title: str
    priority: TicketPriority
    status: TicketStatus = TicketStatus.OPEN
    owner_id: int | None = None

    def __post_init__(self) -> None:
        if type(self.ticket_id) is not int:
            raise TypeError("ticket_id must be an int")

        if not isinstance(self.priority, TicketPriority):
            raise TypeError("priority must be a TicketPriority instance")

        if not isinstance(self.status, TicketStatus):
            raise TypeError("status must be a TicketStatus instance")

        self.title = _normalize_ticket_title(self.title)

        if self.ticket_id <= 0:
            raise ValueError("ticket_id must be positive")

        if self.owner_id is not None:
            if type(self.owner_id) is not int:
                raise TypeError("owner_id must be an int or None")

            if self.owner_id <= 0:
                raise ValueError("owner_id must be positive")

    def change_title(self, new_title: str) -> None:
        normalized = _normalize_ticket_title(new_title)
        self.title = normalized

    def change_priority(self, new_priority: TicketPriority) -> None:
        if not isinstance(new_priority, TicketPriority):
            raise TypeError("new_priority must be a TicketPriority instance")
        self.priority = new_priority

    def change_status(self, new_status: TicketStatus) -> None:
        if not isinstance(new_status, TicketStatus):
            raise TypeError("new_status must be a TicketStatus instance")
        self.status = new_status
