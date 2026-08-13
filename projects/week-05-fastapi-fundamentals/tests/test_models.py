import pytest

from ticket_api.models import Ticket, TicketPriority, TicketStatus


def test_ticket_uses_open_status_by_default() -> None:
    ticket = Ticket(
        ticket_id=1,
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
    )

    assert ticket.status is TicketStatus.OPEN


def test_ticket_strips_title_whitespace() -> None:
    ticket = Ticket(
        ticket_id=2,
        title="  VPN connection fails  ",
        priority=TicketPriority.MEDIUM,
    )

    assert ticket.title == "VPN connection fails"


def test_ticket_rejects_non_positive_id() -> None:
    for invalid_id in (0, -1):
        with pytest.raises(ValueError, match="ticket_id"):
            Ticket(
                ticket_id=invalid_id,
                title="VPN connection fails",
                priority=TicketPriority.LOW,
            )


def test_ticket_rejects_string_id() -> None:
    with pytest.raises(TypeError, match="ticket_id"):
        Ticket(ticket_id="3", title="VPN connection fails", priority=TicketPriority.LOW)


def test_ticket_rejects_title_below_minimum_length() -> None:
    with pytest.raises(ValueError, match="title"):
        Ticket(
            ticket_id=4,
            title="AB",
            priority=TicketPriority.LOW,
        )


def test_ticket_rejects_title_above_maximum_length() -> None:
    with pytest.raises(ValueError, match="title"):
        Ticket(
            ticket_id=5,
            title="A" * 101,
            priority=TicketPriority.LOW,
        )


def test_ticket_rejects_non_string_title() -> None:
    with pytest.raises(TypeError, match="title"):
        Ticket(
            ticket_id=6,
            title=123,
            priority=TicketPriority.LOW,
        )


def test_ticket_rejects_raw_string_priority() -> None:
    with pytest.raises(TypeError, match="priority"):
        Ticket(
            ticket_id=7,
            title="VPN connection fails",
            priority="high",
        )


def test_ticket_changes_status() -> None:
    ticket = Ticket(
        ticket_id=8,
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
    )

    ticket.change_status(TicketStatus.IN_PROGRESS)

    assert ticket.status is TicketStatus.IN_PROGRESS


def test_ticket_rejects_raw_string_status_change() -> None:
    ticket = Ticket(
        ticket_id=9,
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
    )

    with pytest.raises(TypeError, match="new_status"):
        ticket.change_status("in_progress")

    assert ticket.status is TicketStatus.OPEN
