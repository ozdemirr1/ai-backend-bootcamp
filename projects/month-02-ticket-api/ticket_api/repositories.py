from typing import Protocol

from ticket_api.models import NewTicket, Ticket
from ticket_api.user_models import (
    NewUser,
    User,
    UserRole,
    normalize_user_email,
)


class TicketRepositoryConflictError(Exception):
    pass


class TicketRepository(Protocol):
    def create(self, ticket: NewTicket) -> Ticket: ...

    def get_by_id(self, ticket_id: int) -> Ticket | None: ...

    def list_by_owner(self, owner_id: int) -> list[Ticket]: ...

    def update(self, ticket: Ticket) -> bool: ...

    def delete(self, ticket_id: int) -> bool: ...


class UserRepositoryConflictError(Exception):
    pass


class UserRepository(Protocol):
    def create(self, user: NewUser) -> User: ...

    def get_by_id(self, user_id: int) -> User | None: ...

    def get_by_email(self, email: str) -> User | None: ...


class InMemoryTicketRepository:
    def __init__(self) -> None:
        self._tickets: dict[int, Ticket] = {}
        self._next_ticket_id = 1

    def create(self, ticket: NewTicket) -> Ticket:
        if not isinstance(ticket, NewTicket):
            raise TypeError("ticket must be a NewTicket instance")

        new_ticket = Ticket(
            ticket_id=self._next_ticket_id,
            title=ticket.title,
            priority=ticket.priority,
            owner_id=ticket.owner_id,
        )

        if not self.add(new_ticket):
            raise TicketRepositoryConflictError(
                f"Ticket {new_ticket.ticket_id} already exists"
            )

        self._next_ticket_id += 1
        return new_ticket

    def add(self, ticket: Ticket) -> bool:
        if not isinstance(ticket, Ticket):
            raise TypeError("ticket must be a Ticket instance")

        if ticket.ticket_id in self._tickets:
            return False

        self._tickets[ticket.ticket_id] = ticket
        return True

    def get_by_id(self, ticket_id: int) -> Ticket | None:
        return self._tickets.get(ticket_id)

    def list_by_owner(self, owner_id: int) -> list[Ticket]:
        return [
            ticket for ticket in self._tickets.values() if ticket.owner_id == owner_id
        ]

    def update(self, ticket: Ticket) -> bool:
        if not isinstance(ticket, Ticket):
            raise TypeError("ticket must be a Ticket instance")

        if ticket.ticket_id not in self._tickets:
            return False

        self._tickets[ticket.ticket_id] = ticket
        return True

    def delete(self, ticket_id: int) -> bool:
        if ticket_id not in self._tickets:
            return False

        del self._tickets[ticket_id]
        return True


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users: dict[int, User] = {}
        self._user_ids_by_email: dict[str, int] = {}
        self._next_user_id = 1

    def create(self, user: NewUser) -> User:
        if not isinstance(user, NewUser):
            raise TypeError("user must be a NewUser instance")

        if user.email in self._user_ids_by_email:
            raise UserRepositoryConflictError(
                f"User with email {user.email} already exists"
            )

        new_user = User(
            user_id=self._next_user_id,
            email=user.email,
            password_hash=user.password_hash,
            role=UserRole.MEMBER,
            is_active=True,
        )

        self._users[new_user.user_id] = new_user
        self._user_ids_by_email[new_user.email] = new_user.user_id

        self._next_user_id += 1
        return new_user

    def get_by_id(self, user_id: int) -> User | None:
        return self._users.get(user_id)

    def get_by_email(self, email: str) -> User | None:
        normalized_email = normalize_user_email(email)
        user_id = self._user_ids_by_email.get(normalized_email)

        if user_id is not None:
            return self._users.get(user_id)

        return None
