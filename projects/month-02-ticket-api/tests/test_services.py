import pytest

from ticket_api.models import Ticket, TicketPriority, TicketStatus
from ticket_api.repositories import InMemoryTicketRepository
from ticket_api.services import (
    DuplicateTicketError,
    TicketNotFoundError,
    TicketService,
)

OWNER_ID = 7


def test_service_creates_and_saves_ticket() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)

    ticket = service.create_ticket(
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
        owner_id=OWNER_ID,
    )

    assert ticket.ticket_id == 1
    assert ticket.owner_id == OWNER_ID
    assert ticket.title == "VPN connection fails"
    assert ticket.priority is TicketPriority.HIGH
    assert ticket.status is TicketStatus.OPEN
    assert repository.get_by_id(1) == ticket


def test_service_assigns_sequential_ticket_ids() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)

    first = service.create_ticket(
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
        owner_id=OWNER_ID,
    )
    second = service.create_ticket(
        title="Email is down",
        priority=TicketPriority.MEDIUM,
        owner_id=OWNER_ID,
    )

    assert first.ticket_id == 1
    assert second.ticket_id == 2


def test_service_does_not_consume_id_when_creation_fails() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)

    with pytest.raises(ValueError, match="title"):
        service.create_ticket(
            title=" ",
            priority=TicketPriority.HIGH,
            owner_id=OWNER_ID,
        )

    assert repository.list_all() == []

    created_ticket = service.create_ticket(
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
        owner_id=OWNER_ID,
    )

    assert created_ticket.ticket_id == 1


def test_service_raises_for_duplicate_ticket_id() -> None:
    repository = InMemoryTicketRepository()
    original = Ticket(
        ticket_id=1,
        title="Existing ticket",
        priority=TicketPriority.LOW,
        owner_id=OWNER_ID,
    )
    repository.add(original)

    service = TicketService(repository)

    with pytest.raises(DuplicateTicketError, match="1"):
        service.create_ticket(
            title="Duplicate ticket",
            priority=TicketPriority.HIGH,
            owner_id=OWNER_ID,
        )

    assert repository.get_by_id(1) == original


def test_service_lists_tickets() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)

    first_ticket = service.create_ticket(
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
        owner_id=OWNER_ID,
    )
    second_ticket = service.create_ticket(
        title="Email is down",
        priority=TicketPriority.MEDIUM,
        owner_id=OWNER_ID,
    )

    assert service.list_tickets() == [first_ticket, second_ticket]


def test_service_gets_existing_ticket() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)

    created_ticket = service.create_ticket(
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
        owner_id=OWNER_ID,
    )

    assert service.get_ticket(created_ticket.ticket_id) == created_ticket


def test_service_raises_when_ticket_is_missing() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)

    with pytest.raises(TicketNotFoundError, match="999"):
        service.get_ticket(999)


def test_service_deletes_existing_ticket() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)

    created_ticket = service.create_ticket(
        title="VPN connection fails",
        priority=TicketPriority.HIGH,
        owner_id=OWNER_ID,
    )

    result = service.delete_ticket(created_ticket.ticket_id)

    assert result is None
    assert repository.get_by_id(created_ticket.ticket_id) is None


def test_service_raises_when_delete_target_is_missing() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)

    with pytest.raises(TicketNotFoundError, match="999"):
        service.delete_ticket(999)


def test_service_does_not_save_ticket_with_raw_string_priority() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)

    with pytest.raises(TypeError, match="priority"):
        service.create_ticket(
            title="VPN connection fails",
            priority="high",  # type: ignore[arg-type]
            owner_id=OWNER_ID,
        )

    assert repository.list_all() == []


def test_service_updates_only_ticket_title() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)
    ticket = service.create_ticket(
        title="Old Title",
        priority=TicketPriority.LOW,
        owner_id=OWNER_ID,
    )

    updated = service.update_ticket(ticket.ticket_id, title="New Title")

    assert updated.title == "New Title"
    assert updated.priority is TicketPriority.LOW
    assert updated.status is TicketStatus.OPEN


def test_service_updates_ticket_priority() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)
    ticket = service.create_ticket(
        title="Old Title",
        priority=TicketPriority.LOW,
        owner_id=OWNER_ID,
    )

    updated = service.update_ticket(ticket.ticket_id, priority=TicketPriority.HIGH)

    assert updated.title == "Old Title"
    assert updated.priority is TicketPriority.HIGH
    assert updated.status is TicketStatus.OPEN


def test_service_updates_ticket_status() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)
    ticket = service.create_ticket(
        title="Old Title",
        priority=TicketPriority.LOW,
        owner_id=OWNER_ID,
    )

    updated = service.update_ticket(ticket.ticket_id, status=TicketStatus.IN_PROGRESS)

    assert updated.title == "Old Title"
    assert updated.priority is TicketPriority.LOW
    assert updated.status is TicketStatus.IN_PROGRESS


def test_service_updates_multiple_ticket_fields() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)
    ticket = service.create_ticket(
        title="Old Title",
        priority=TicketPriority.LOW,
        owner_id=OWNER_ID,
    )

    updated = service.update_ticket(
        ticket.ticket_id, title="New Title", status=TicketStatus.RESOLVED
    )

    assert updated.title == "New Title"
    assert updated.priority is TicketPriority.LOW
    assert updated.status is TicketStatus.RESOLVED


def test_service_persists_updated_ticket() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)
    ticket = service.create_ticket(
        title="Old Title",
        priority=TicketPriority.LOW,
        owner_id=OWNER_ID,
    )

    updated = service.update_ticket(ticket.ticket_id, title="New Title")

    assert repository.get_by_id(ticket.ticket_id) == updated


def test_service_raises_when_update_target_is_missing() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)

    with pytest.raises(TicketNotFoundError, match="999"):
        service.update_ticket(999, title="New Title")


def test_service_preserves_ticket_when_title_update_is_invalid() -> None:
    repository = InMemoryTicketRepository()
    service = TicketService(repository)
    ticket = service.create_ticket(
        title="Old Title",
        priority=TicketPriority.LOW,
        owner_id=OWNER_ID,
    )

    with pytest.raises(ValueError, match="title"):
        service.update_ticket(ticket.ticket_id, title=" ")

    assert ticket.title == "Old Title"
