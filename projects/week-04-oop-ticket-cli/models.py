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


@dataclass
class Ticket:
    ticket_id: int
    title: str
    priority: TicketPriority
    status: TicketStatus = TicketStatus.OPEN

    def __post_init__(self) -> None:
        if self.ticket_id <= 0:
            raise ValueError("ticket_id must be positive")
        if not self.title.strip():
            raise ValueError("title cannot be empty")
        if not isinstance(self.priority, TicketPriority):
            raise TypeError("priority must be an instance of TicketPriority")
        if not isinstance(self.status, TicketStatus):
            raise TypeError("status must be an instance of TicketStatus")

    def get_summary(self) -> str:
        return (
            f"Ticket {self.ticket_id}: {self.title} | "
            f"Priority: {self.priority.value} | "
            f"Status: {self.status.value}"
        )

    def change_status(self, new_status: TicketStatus) -> None:
        if not isinstance(new_status, TicketStatus):
            raise TypeError("new_status must be an instance of TicketStatus")
        self.status = new_status
