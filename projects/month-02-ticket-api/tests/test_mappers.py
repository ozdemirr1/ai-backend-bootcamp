from datetime import UTC, datetime

import pytest

from ticket_api.mappers import (
    new_user_to_record,
    ticket_record_to_domain,
    update_ticket_record_from_domain,
    user_record_to_domain,
)
from ticket_api.models import Ticket, TicketPriority, TicketStatus
from ticket_api.persistence_models import TicketRecord, UserRecord
from ticket_api.user_models import NewUser, User, UserRole


def test_ticket_record_to_domain_converts_persistence_values() -> None:
    record = TicketRecord(
        ticket_id=1,
        title="VPN connection fails",
        priority="high",
        status="in_progress",
    )

    ticket = ticket_record_to_domain(record)

    assert isinstance(ticket, Ticket)
    assert ticket.ticket_id == 1
    assert ticket.title == "VPN connection fails"
    assert ticket.priority == TicketPriority.HIGH
    assert ticket.status == TicketStatus.IN_PROGRESS


def test_ticket_record_to_domain_rejects_invalid_priority() -> None:
    record = TicketRecord(
        ticket_id=1,
        title="VPN connection fails",
        priority="urgent",
        status="in_progress",
    )

    with pytest.raises(ValueError):
        ticket_record_to_domain(record)


def test_ticket_record_to_domain_rejects_invalid_status() -> None:
    record = TicketRecord(
        ticket_id=1,
        title="VPN connection fails",
        priority="high",
        status="pending",
    )

    with pytest.raises(ValueError):
        ticket_record_to_domain(record)


def test_update_ticket_record_from_domain_updates_business_fields() -> None:
    timestamp = datetime(2026, 8, 25, 12, 0, tzinfo=UTC)
    record = TicketRecord(
        ticket_id=1,
        title="Old title",
        priority="low",
        status="open",
        created_at=timestamp,
        updated_at=timestamp,
    )
    ticket = Ticket(
        ticket_id=1,
        title="New title",
        priority=TicketPriority.CRITICAL,
        status=TicketStatus.RESOLVED,
    )

    update_ticket_record_from_domain(record, ticket)

    assert record.ticket_id == 1
    assert record.title == "New title"
    assert record.priority == "critical"
    assert record.status == "resolved"
    assert record.created_at == timestamp
    assert record.updated_at == timestamp


def test_update_ticket_record_from_domain_rejects_mismatched_identifiers() -> None:
    record = TicketRecord(
        ticket_id=1,
        title="Old title",
        priority="low",
        status="open",
    )
    ticket = Ticket(
        ticket_id=2,
        title="New title",
        priority=TicketPriority.CRITICAL,
        status=TicketStatus.RESOLVED,
    )

    with pytest.raises(ValueError, match="record and domain identifiers must match"):
        update_ticket_record_from_domain(record, ticket)

    assert record.ticket_id == 1
    assert record.title == "Old title"
    assert record.priority == "low"
    assert record.status == "open"


def test_new_user_to_record_maps_only_registration_fields() -> None:
    new_user = NewUser(
        email="Furkan@Example.com",
        password_hash="$argon2id$example",
    )

    record = new_user_to_record(new_user)

    assert isinstance(record, UserRecord)
    assert record.user_id is None
    assert record.email == "furkan@example.com"
    assert record.password_hash == "$argon2id$example"
    assert record.role is None
    assert record.is_active is None


def test_user_record_to_domain_converts_persistence_values() -> None:
    record = UserRecord(
        user_id=7,
        email="furkan@example.com",
        password_hash="$argon2id$example",
        role="admin",
        is_active=False,
    )

    user = user_record_to_domain(record)

    assert isinstance(user, User)
    assert user.user_id == 7
    assert user.email == "furkan@example.com"
    assert user.password_hash == "$argon2id$example"
    assert user.role is UserRole.ADMIN
    assert user.is_active is False


def test_user_record_to_domain_rejects_invalid_role() -> None:
    record = UserRecord(
        user_id=7,
        email="furkan@example.com",
        password_hash="$argon2id$example",
        role="superadmin",
        is_active=True,
    )

    with pytest.raises(ValueError):
        user_record_to_domain(record)


def test_new_user_to_record_rejects_wrong_type() -> None:
    with pytest.raises(TypeError, match="NewUser"):
        new_user_to_record("not-a-user")  # type: ignore[arg-type]


def test_user_record_to_domain_rejects_wrong_type() -> None:
    with pytest.raises(TypeError, match="UserRecord"):
        user_record_to_domain("not-a-record")  # type: ignore[arg-type]
