import pytest

from ticket_api.models import NewTicket, Ticket, TicketPriority, TicketStatus


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
            title=123,  # type: ignore[arg-type]
            priority=TicketPriority.LOW,
        )


def test_ticket_rejects_raw_string_priority() -> None:
    with pytest.raises(TypeError, match="priority"):
        Ticket(
            ticket_id=7,
            title="VPN connection fails",
            priority="high",  # type: ignore[arg-type]
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
        ticket.change_status("in_progress")  # type: ignore[arg-type]

    assert ticket.status is TicketStatus.OPEN


def test_ticket_changes_title() -> None:
    ticket = Ticket(
        ticket_id=1,
        title="Old Title",
        priority=TicketPriority.HIGH,
    )

    ticket.change_title("  New Title  ")

    assert ticket.title == "New Title"


def test_ticket_preserves_title_when_change_is_invalid() -> None:
    ticket = Ticket(
        ticket_id=1,
        title="Old Title",
        priority=TicketPriority.HIGH,
    )

    with pytest.raises(ValueError, match="title"):
        ticket.change_title(" ")

    assert ticket.title == "Old Title"


def test_ticket_changes_priority() -> None:
    ticket = Ticket(
        ticket_id=1,
        title="VPN connection fails",
        priority=TicketPriority.LOW,
    )

    ticket.change_priority(TicketPriority.CRITICAL)

    assert ticket.priority is TicketPriority.CRITICAL


def test_ticket_preserves_priority_when_change_is_invalid() -> None:
    ticket = Ticket(
        ticket_id=1,
        title="VPN connection fails",
        priority=TicketPriority.LOW,
    )

    with pytest.raises(TypeError, match="new_priority"):
        ticket.change_priority("critical")  # type: ignore[arg-type]

    assert ticket.priority is TicketPriority.LOW


def test_new_ticket_strips_title_whitespace() -> None:
    ticket = NewTicket(
        title=" VPN connection fails ",
        priority=TicketPriority.MEDIUM,
        owner_id=7,
    )

    assert ticket.title == "VPN connection fails"


def test_new_ticket_rejects_invalid_short_title() -> None:
    with pytest.raises(ValueError, match="title"):
        NewTicket(
            title="AB",
            priority=TicketPriority.MEDIUM,
            owner_id=7,
        )


def test_new_ticket_rejects_raw_string_priority() -> None:
    with pytest.raises(TypeError, match="priority"):
        NewTicket(
            title="VPN connection fails",
            priority="high",  # type: ignore[arg-type]
            owner_id=7,
        )


def test_ticket_allows_missing_owner_during_migration() -> None:
    ticket = Ticket(
        ticket_id=1,
        title="Legacy ticket",
        priority=TicketPriority.LOW,
    )

    assert ticket.owner_id is None


def test_ticket_accepts_positive_owner_id() -> None:
    ticket = Ticket(
        ticket_id=1,
        title="Owned ticket",
        priority=TicketPriority.HIGH,
        owner_id=7,
    )

    assert ticket.owner_id == 7


@pytest.mark.parametrize(
    ("owner_id", "expected_exception"),
    [
        (0, ValueError),
        (-1, ValueError),
        ("7", TypeError),
        (True, TypeError),
    ],
)
def test_ticket_rejects_invalid_owner_id(
    owner_id: object,
    expected_exception: type[Exception],
) -> None:
    with pytest.raises(expected_exception, match="owner_id"):
        Ticket(
            ticket_id=1,
            title="Owned ticket",
            priority=TicketPriority.HIGH,
            owner_id=owner_id,  # type: ignore[arg-type]
        )


def test_new_ticket_requires_owner_id() -> None:
    with pytest.raises(TypeError, match="owner_id"):
        NewTicket(
            title="Owned ticket",
            priority=TicketPriority.HIGH,
        )  # type: ignore[call-arg]


def test_new_ticket_accepts_positive_owner_id() -> None:
    ticket = NewTicket(
        title="Owned ticket",
        priority=TicketPriority.HIGH,
        owner_id=7,
    )

    assert ticket.owner_id == 7


@pytest.mark.parametrize(
    ("owner_id", "expected_exception"),
    [
        (0, ValueError),
        (-1, ValueError),
        ("7", TypeError),
        (True, TypeError),
    ],
)
def test_new_ticket_rejects_invalid_owner_id(
    owner_id: object,
    expected_exception: type[Exception],
) -> None:
    with pytest.raises(expected_exception, match="owner_id"):
        NewTicket(
            title="Owned ticket",
            priority=TicketPriority.HIGH,
            owner_id=owner_id,  # type: ignore[arg-type]
        )
