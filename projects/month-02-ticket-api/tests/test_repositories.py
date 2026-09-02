import pytest

from ticket_api.models import NewTicket, Ticket, TicketPriority, TicketStatus
from ticket_api.repositories import (
    InMemoryTicketRepository,
    InMemoryUserRepository,
    TicketRepositoryConflictError,
    UserRepositoryConflictError,
)
from ticket_api.user_models import NewUser, UserRole


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


def test_repository_creates_ticket_and_generates_id() -> None:
    repo = InMemoryTicketRepository()
    new_ticket = NewTicket(title="VPN connection fails", priority=TicketPriority.HIGH)

    ticket = repo.create(new_ticket)

    assert ticket.ticket_id == 1
    assert ticket.title == "VPN connection fails"
    assert ticket.priority is TicketPriority.HIGH


def test_repository_generates_consecutive_ids() -> None:
    repo = InMemoryTicketRepository()
    t1 = repo.create(NewTicket(title="First Ticket", priority=TicketPriority.LOW))
    t2 = repo.create(NewTicket(title="Second Ticket", priority=TicketPriority.MEDIUM))

    assert t1.ticket_id == 1
    assert t2.ticket_id == 2


def test_repository_create_rejects_invalid_type() -> None:
    repo = InMemoryTicketRepository()

    with pytest.raises(TypeError, match="ticket must be a NewTicket instance"):
        repo.create(Ticket(ticket_id=1, title="Test", priority=TicketPriority.LOW))


def test_repository_create_raises_conflict_if_id_exists() -> None:
    repo = InMemoryTicketRepository()

    repo.add(Ticket(ticket_id=1, title="Manual Ticket", priority=TicketPriority.LOW))

    new_ticket = NewTicket(title="Conflicting Ticket", priority=TicketPriority.HIGH)

    with pytest.raises(TicketRepositoryConflictError):
        repo.create(new_ticket)


def test_repository_update_stores_modified_ticket() -> None:
    repo = InMemoryTicketRepository()
    ticket = repo.create(NewTicket(title="Old Title", priority=TicketPriority.LOW))

    ticket.change_title("New Title")
    ticket.change_status(TicketStatus.IN_PROGRESS)

    success = repo.update(ticket)

    assert success is True
    saved = repo.get_by_id(ticket.ticket_id)
    assert saved is not None
    assert saved.title == "New Title"
    assert saved.status is TicketStatus.IN_PROGRESS


def test_repository_update_returns_false_for_missing_id() -> None:
    repo = InMemoryTicketRepository()
    ticket = Ticket(ticket_id=999, title="Not in repo", priority=TicketPriority.LOW)

    assert repo.update(ticket) is False


def test_repository_update_rejects_invalid_type() -> None:
    repo = InMemoryTicketRepository()

    with pytest.raises(TypeError, match="ticket must be a Ticket instance"):
        repo.update(NewTicket(title="Test", priority=TicketPriority.LOW))


def test_user_repository_creates_member_with_generated_id() -> None:
    repository = InMemoryUserRepository()
    new_user = NewUser(
        email="Furkan@Example.com",
        password_hash="$argon2id$example",
    )

    user = repository.create(new_user)

    assert user.user_id == 1
    assert user.email == "furkan@example.com"
    assert user.password_hash == "$argon2id$example"
    assert user.role is UserRole.MEMBER
    assert user.is_active is True


def test_user_repository_generates_consecutive_ids() -> None:
    repository = InMemoryUserRepository()

    u1 = repository.create(NewUser(email="first@example.com", password_hash="hash1"))
    u2 = repository.create(NewUser(email="second@example.com", password_hash="hash2"))

    assert u1.user_id == 1
    assert u2.user_id == 2


def test_user_repository_gets_user_by_id() -> None:
    repository = InMemoryUserRepository()
    user = repository.create(
        NewUser(email="furkan@example.com", password_hash="$argon2id$example")
    )

    found = repository.get_by_id(user.user_id)

    assert found == user


def test_user_repository_gets_user_by_normalized_email() -> None:
    repository = InMemoryUserRepository()
    user = repository.create(
        NewUser(email="furkan@example.com", password_hash="$argon2id$example")
    )

    found = repository.get_by_email(" FURKAN@example.com ")

    assert found == user


def test_user_repository_returns_none_for_missing_user() -> None:
    repository = InMemoryUserRepository()

    assert repository.get_by_id(999) is None
    assert repository.get_by_email("missing@example.com") is None


def test_user_repository_rejects_duplicate_normalized_email() -> None:
    repository = InMemoryUserRepository()
    repository.create(
        NewUser(
            email="furkan@example.com",
            password_hash="$argon2id$first",
        )
    )

    with pytest.raises(UserRepositoryConflictError):
        repository.create(
            NewUser(
                email=" FURKAN@EXAMPLE.COM ",
                password_hash="$argon2id$second",
            )
        )


def test_user_repository_create_rejects_invalid_type() -> None:
    repository = InMemoryUserRepository()

    with pytest.raises(TypeError, match="user must be a NewUser instance"):
        repository.create("not-a-new-user")
