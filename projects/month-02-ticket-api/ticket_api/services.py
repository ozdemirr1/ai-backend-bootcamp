from typing import Protocol

from ticket_api.models import NewTicket, Ticket, TicketPriority, TicketStatus
from ticket_api.repositories import (
    TicketRepository,
    TicketRepositoryConflictError,
    UserRepository,
    UserRepositoryConflictError,
)
from ticket_api.user_models import (
    NewUser,
    User,
    normalize_user_email,
)


class PasswordHashing(Protocol):
    def hash_password(self, plain_password: str) -> str: ...


class PasswordVerifying(Protocol):
    def verify_password(
        self,
        plain_password: str,
        password_hash: str,
    ) -> bool: ...


class AccessTokenIssuing(Protocol):
    def create_access_token(self, user_id: int) -> str: ...


class InvalidCredentialsError(Exception):
    pass


class TicketNotFoundError(Exception):
    pass


class DuplicateTicketError(Exception):
    pass


class DuplicateUserError(Exception):
    pass


class RegistrationService:
    def __init__(
        self,
        repository: UserRepository,
        password_hasher: PasswordHashing,
    ) -> None:
        self._repository = repository
        self._password_hasher = password_hasher

    def register_user(
        self,
        email: str,
        plain_password: str,
    ) -> User:
        normalized_email = normalize_user_email(email)

        password_hash = self._password_hasher.hash_password(plain_password)

        new_user = NewUser(
            email=normalized_email,
            password_hash=password_hash,
        )

        try:
            return self._repository.create(new_user)
        except UserRepositoryConflictError as exc:
            raise DuplicateUserError("User registration conflict") from exc


class AuthenticationService:
    def __init__(
        self,
        repository: UserRepository,
        password_verifier: PasswordVerifying,
        token_issuer: AccessTokenIssuing,
        dummy_password_hash: str,
    ) -> None:
        self._repository = repository
        self._password_verifier = password_verifier
        self._token_issuer = token_issuer
        self._dummy_password_hash = dummy_password_hash

    def login_user(
        self,
        email: str,
        plain_password: str,
    ) -> str:
        normalized_email = normalize_user_email(email)
        user = self._repository.get_by_email(normalized_email)

        password_hash = (
            user.password_hash if user is not None else self._dummy_password_hash
        )

        password_matches = self._password_verifier.verify_password(
            plain_password,
            password_hash,
        )

        if user is None or not password_matches or not user.is_active:
            raise InvalidCredentialsError("Invalid email or password")

        return self._token_issuer.create_access_token(user.user_id)


class TicketService:
    def __init__(self, repository: TicketRepository) -> None:
        self._repository = repository

    def create_ticket(self, title: str, priority: TicketPriority) -> Ticket:
        new_ticket = NewTicket(
            title=title,
            priority=priority,
        )

        try:
            return self._repository.create(new_ticket)
        except TicketRepositoryConflictError as exc:
            raise DuplicateTicketError(str(exc)) from exc

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

    def update_ticket(
        self,
        ticket_id: int,
        *,
        title: str | None = None,
        priority: TicketPriority | None = None,
        status: TicketStatus | None = None,
    ) -> Ticket:
        ticket = self.get_ticket(ticket_id)

        if title is not None:
            ticket.change_title(title)

        if priority is not None:
            ticket.change_priority(priority)

        if status is not None:
            ticket.change_status(status)

        if not self._repository.update(ticket):
            raise TicketNotFoundError(f"Ticket {ticket_id} not found")

        return ticket
