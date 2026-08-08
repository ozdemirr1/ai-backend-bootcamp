from typing import Optional

from models import Ticket


class TicketRepository:
    def __init__(self) -> None:
        self._tickets: list[Ticket] = []

    def save(self, ticket: Ticket) -> None:
        self._tickets.append(ticket)

    def list_all(self) -> list[Ticket]:
        return list(self._tickets)

    def find_by_id(self, ticket_id: int) -> Optional[Ticket]:
        for ticket in self._tickets:
            if ticket.ticket_id == ticket_id:
                return ticket
        return None
