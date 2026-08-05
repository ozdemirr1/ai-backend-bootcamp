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
