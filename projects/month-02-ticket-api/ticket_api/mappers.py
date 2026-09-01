from ticket_api.models import Ticket, TicketPriority, TicketStatus
from ticket_api.persistence_models import TicketRecord, UserRecord
from ticket_api.user_models import NewUser, User, UserRole


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


def new_user_to_record(user: NewUser) -> UserRecord:
    if not isinstance(user, NewUser):
        raise TypeError("user must be a NewUser instance")

    return UserRecord(
        email=user.email,
        password_hash=user.password_hash,
    )


def user_record_to_domain(record: UserRecord) -> User:
    if not isinstance(record, UserRecord):
        raise TypeError("record must be a UserRecord instance")

    return User(
        user_id=record.user_id,
        email=record.email,
        password_hash=record.password_hash,
        role=UserRole(record.role),
        is_active=record.is_active,
    )
