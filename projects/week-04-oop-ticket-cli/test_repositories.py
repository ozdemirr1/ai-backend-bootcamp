from models import Ticket, TicketPriority
from repositories import TicketRepository


def test_repository_saves_ticket() -> None:
    repository = TicketRepository()
    ticket = Ticket(
        ticket_id=1001,
        title="Test Ticket",
        priority=TicketPriority.HIGH,
    )
    repository.save(ticket)
    assert repository.list_all() == [ticket]


def test_repository_list_all_returns_a_copy() -> None:
    repository = TicketRepository()
    ticket = Ticket(
        ticket_id=1002,
        title="Test Ticket",
        priority=TicketPriority.HIGH,
    )
    repository.save(ticket)

    returned_tickets = repository.list_all()
    returned_tickets.clear()

    assert repository.list_all() == [ticket]


def test_repository_finds_ticket_by_id() -> None:
    repository = TicketRepository()
    ticket = Ticket(
        ticket_id=1003,
        title="Test Ticket",
        priority=TicketPriority.MEDIUM,
    )
    repository.save(ticket)

    found_ticket = repository.find_by_id(1003)
    assert found_ticket == ticket


def test_repository_returns_none_when_ticket_is_missing() -> None:
    repository = TicketRepository()
    ticket = Ticket(
        ticket_id=1004,
        title="Test Ticket",
        priority=TicketPriority.LOW,
    )
    repository.save(ticket)

    found_ticket = repository.find_by_id(9999)
    assert found_ticket is None
