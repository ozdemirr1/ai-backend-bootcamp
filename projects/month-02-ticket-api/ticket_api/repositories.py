from typing import Protocol

from ticket_api.models import NewTicket, Ticket


class TicketRepositoryConflictError(Exception):
    pass


class TicketRepository(Protocol):
    def create(self, ticket: NewTicket) -> Ticket: ...

    def get_by_id(self, ticket_id: int) -> Ticket | None: ...

    def list_all(self) -> list[Ticket]: ...

    def update(self, ticket: Ticket) -> bool: ...

    def delete(self, ticket_id: int) -> bool: ...


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

    def list_all(self) -> list[Ticket]:
        return list(self._tickets.values())

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
