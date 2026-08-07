import pytest
from models import TicketPriority, TicketStatus
from repositories import TicketRepository
from services import TicketService


def test_service_creates_and_saves_ticket() -> None:
    repository = TicketRepository()
    service = TicketService(repository)

    created_ticket = service.create_ticket(
        ticket_id=1001,
        title="Test Ticket",
        priority=TicketPriority.CRITICAL,
    )

    assert created_ticket.ticket_id == 1001
    assert created_ticket.title == "Test Ticket"
    assert created_ticket.priority == TicketPriority.CRITICAL
    assert created_ticket.status == TicketStatus.OPEN
    assert repository.list_all() == [created_ticket]


def test_service_rejects_duplicate_ticket_id() -> None:
    repository = TicketRepository()
    service = TicketService(repository)

    service.create_ticket(
        ticket_id=1001,
        title="First Ticket",
        priority=TicketPriority.HIGH,
    )

    with pytest.raises(ValueError) as exc_info:
        service.create_ticket(
            ticket_id=1001,
            title="Duplicate Ticket",
            priority=TicketPriority.LOW,
        )

    assert str(exc_info.value) == "Ticket with ID 1001 already exists."
    assert len(repository.list_all()) == 1


def test_service_does_not_save_ticket_when_title_is_invalid() -> None:
    repository = TicketRepository()
    service = TicketService(repository)

    with pytest.raises(ValueError, match="title"):
        service.create_ticket(ticket_id=1006, title="  ", priority=TicketPriority.HIGH)

    assert repository.list_all() == []


def test_service_lists_created_tickets() -> None:
    repository = TicketRepository()
    service = TicketService(repository)

    first_ticket = service.create_ticket(
        ticket_id=1007,
        title="First Ticket",
        priority=TicketPriority.HIGH,
    )
    second_ticket = service.create_ticket(
        ticket_id=1008,
        title="Second Ticket",
        priority=TicketPriority.LOW,
    )

    tickets = service.list_tickets()
    assert tickets == [first_ticket, second_ticket]
