from ticket_api.models import Ticket


class InMemoryTicketRepository:
    def __init__(self) -> None:
        self._tickets: dict[int, Ticket] = {}

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

    def delete(self, ticket_id: int) -> bool:
        if ticket_id not in self._tickets:
            return False

        del self._tickets[ticket_id]
        return True
