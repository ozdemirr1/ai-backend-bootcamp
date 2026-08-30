from ticket_api.models import Ticket, TicketPriority, TicketStatus
from ticket_api.persistence_models import TicketRecord


def ticket_record_to_domain(record: TicketRecord) -> Ticket:
    return Ticket(
        ticket_id=record.ticket_id,
        title=record.title,
        priority=TicketPriority(record.priority),
        status=TicketStatus(record.status),
    )


def update_ticket_record_from_domain(
    record: TicketRecord,
    ticket: Ticket,
) -> None:
    if record.ticket_id != ticket.ticket_id:
        raise ValueError("record and domain identifiers must match")

    record.title = ticket.title
    record.priority = ticket.priority.value
    record.status = ticket.status.value
