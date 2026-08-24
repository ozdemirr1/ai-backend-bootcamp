import pytest

from ticket_api.models import Ticket, TicketPriority
from ticket_api.repositories import InMemoryTicketRepository


def test_repository_adds_ticket() -> None:
    repository = InMemoryTicketRepository()
    ticket = Ticket(
        ticket_id=1,
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
    )

    result = repository.add(ticket)

    assert result is True
    assert repository.get_by_id(1) == ticket


def test_repository_rejects_non_ticket() -> None:
    repository = InMemoryTicketRepository()

    with pytest.raises(TypeError, match="ticket"):
        repository.add("not-a-ticket")


def test_repository_rejects_duplicate_ticket_id() -> None:
    repository = InMemoryTicketRepository()
    original = Ticket(
        ticket_id=2,
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
    )

    duplicate = Ticket(
        ticket_id=2,
        title="Email is down",
        priority=TicketPriority.MEDIUM,
    )

    repository.add(original)
    result = repository.add(duplicate)

    assert result is False
    assert repository.get_by_id(2) == original


def test_repository_returns_none_for_missing_ticket() -> None:
    repository = InMemoryTicketRepository()

    assert repository.get_by_id(999) is None


def test_repository_lists_all_tickets() -> None:
    repository = InMemoryTicketRepository()
    ticket1 = Ticket(
        ticket_id=3,
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
    )
    ticket2 = Ticket(
        ticket_id=4,
        title="Email is down",
        priority=TicketPriority.MEDIUM,
    )

    repository.add(ticket1)
    repository.add(ticket2)

    assert repository.list_all() == [ticket1, ticket2]


def test_repository_list_all_returns_a_new_list() -> None:
    repository = InMemoryTicketRepository()
    ticket = Ticket(
        ticket_id=5,
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
    )
    repository.add(ticket)

    returned_tickets = repository.list_all()
    returned_tickets.clear()

    assert repository.list_all() == [ticket]


def test_repository_deletes_existing_ticket() -> None:
    repository = InMemoryTicketRepository()
    ticket = Ticket(
        ticket_id=6,
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
    )
    repository.add(ticket)

    result = repository.delete(6)

    assert result is True
    assert repository.get_by_id(6) is None


def test_repository_returns_false_when_delete_target_is_missing() -> None:
    repository = InMemoryTicketRepository()

    result = repository.delete(999)

    assert result is False
