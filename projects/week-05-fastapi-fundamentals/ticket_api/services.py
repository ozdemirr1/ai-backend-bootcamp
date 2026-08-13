from ticket_api.models import Ticket, TicketPriority
from ticket_api.repositories import InMemoryTicketRepository


class TicketNotFoundError(Exception):
    pass


class DuplicateTicketError(Exception):
    pass


class TicketService:
    def __init__(self, repository: InMemoryTicketRepository) -> None:
        self._repository = repository
        self._next_ticket_id = 1

    def create_ticket(self, title: str, priority: TicketPriority) -> Ticket:
        ticket = Ticket(
            ticket_id=self._next_ticket_id,
            title=title,
            priority=priority,
        )

        if not self._repository.add(ticket):
            raise DuplicateTicketError(f"Ticket {ticket.ticket_id} already exists")

        self._next_ticket_id += 1
        return ticket

    def list_tickets(self) -> list[Ticket]:
        return self._repository.list_all()

    def get_ticket(self, ticket_id: int) -> Ticket:
        ticket = self._repository.get_by_id(ticket_id)

        if ticket is None:
            raise TicketNotFoundError(f"Ticket {ticket_id} not found")

        return ticket

    def delete_ticket(self, ticket_id: int) -> None:
        if not self._repository.delete(ticket_id):
            raise TicketNotFoundError(f"Ticket {ticket_id} not found")
