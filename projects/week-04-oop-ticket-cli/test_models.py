import pytest
from models import Ticket, TicketPriority, TicketStatus


def test_ticket_uses_open_status_by_default() -> None:
    ticket = Ticket(
        ticket_id=1001,
        title="Password reset problem",
        priority=TicketPriority.HIGH
    )
    assert ticket.status is TicketStatus.OPEN


def test_ticket_rejects_empty_title() -> None:
    with pytest.raises(ValueError, match="title"):
        Ticket(
            ticket_id=1002,
            title="  ",
            priority=TicketPriority.MEDIUM
        )


def test_ticket_rejects_raw_string_priority() -> None:
    with pytest.raises(TypeError, match="priority"):
        Ticket(
            ticket_id=1003,
            title="VPN connection fails",
            priority="high"
        )


def test_ticket_rejects_raw_string_status() -> None:
    with pytest.raises(TypeError, match="status"):
        Ticket(
            ticket_id=1004,
            title="Email not syncing",
            priority=TicketPriority.LOW,
            status="open"
        )


def test_ticket_rejects_non_positive_id() -> None:
    with pytest.raises(ValueError, match="ticket_id"):
        Ticket(
            ticket_id=0,
            title="Invalid ticket ID",
            priority=TicketPriority.LOW
        )


def test_ticket_summary_uses_enum_values() -> None:
    ticket = Ticket(
        ticket_id=1005,
        title="Printer is offline",
        priority=TicketPriority.CRITICAL,
        status=TicketStatus.IN_PROGRESS
    )

    result = ticket.get_summary()

    assert result == (
    "Ticket 1005: Printer is offline | "
    "Priority: critical | "
    "Status: in_progress"
    )