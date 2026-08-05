from models import Ticket, TicketPriority
from repositories import TicketRepository


class TicketService:
    def __init__(self, repository: TicketRepository) -> None:
        self._repository = repository

    def create_ticket(self, ticket_id: int, title: str, priority: TicketPriority) -> Ticket:
        existing_ticket = self._repository.find_by_id(ticket_id)

        if existing_ticket is not None:
            raise ValueError(f"Ticket with ID {ticket_id} already exists.")

        ticket = Ticket(ticket_id=ticket_id, title=title, priority=priority)
        self._repository.save(ticket)
        return ticket
