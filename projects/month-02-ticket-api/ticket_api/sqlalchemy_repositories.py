from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ticket_api.mappers import (
    new_user_to_record,
    ticket_record_to_domain,
    update_ticket_record_from_domain,
    user_record_to_domain,
)
from ticket_api.models import NewTicket, Ticket
from ticket_api.persistence_models import TicketRecord, UserRecord
from ticket_api.repositories import (
    TicketRepositoryConflictError,
    UserRepositoryConflictError,
)
from ticket_api.user_models import (
    NewUser,
    User,
    normalize_user_email,
)


class SqlAlchemyTicketRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, ticket: NewTicket) -> Ticket:
        if not isinstance(ticket, NewTicket):
            raise TypeError("ticket must be a NewTicket instance")

        record = TicketRecord(
            owner_id=ticket.owner_id,
            title=ticket.title,
            priority=ticket.priority.value,
        )

        self._session.add(record)

        try:
            self._session.flush()
        except IntegrityError as exc:
            raise TicketRepositoryConflictError("Ticket persistence conflict") from exc

        self._session.refresh(record)

        return ticket_record_to_domain(record)

    def get_by_id(self, ticket_id: int) -> Ticket | None:
        record = self._session.get(TicketRecord, ticket_id)
        if record is None:
            return None

        return ticket_record_to_domain(record)

    def list_all(self) -> list[Ticket]:
        statement = select(TicketRecord).order_by(TicketRecord.ticket_id.asc())
        records = self._session.scalars(statement).all()

        return [ticket_record_to_domain(record) for record in records]

    def update(self, ticket: Ticket) -> bool:
        if not isinstance(ticket, Ticket):
            raise TypeError("ticket must be a Ticket instance")

        record = self._session.get(TicketRecord, ticket.ticket_id)
        if record is None:
            return False

        update_ticket_record_from_domain(record, ticket)

        self._session.flush()
        self._session.refresh(record)

        return True

    def delete(self, ticket_id: int) -> bool:
        record = self._session.get(TicketRecord, ticket_id)
        if record is None:
            return False

        self._session.delete(record)
        self._session.flush()

        return True


class SqlAlchemyUserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, user: NewUser) -> User:
        if not isinstance(user, NewUser):
            raise TypeError("user must be a NewUser instance")

        record = new_user_to_record(user)
        self._session.add(record)

        try:
            self._session.flush()
        except IntegrityError as exc:
            raise UserRepositoryConflictError("User persistence conflict") from exc

        self._session.refresh(record)

        return user_record_to_domain(record)

    def get_by_id(self, user_id: int) -> User | None:
        record = self._session.get(UserRecord, user_id)

        if record is None:
            return None

        return user_record_to_domain(record)

    def get_by_email(self, email: str) -> User | None:
        normalized_email = normalize_user_email(email)

        statement = select(UserRecord).where(UserRecord.email == normalized_email)
        record = self._session.scalar(statement)

        if record is None:
            return None

        return user_record_to_domain(record)
