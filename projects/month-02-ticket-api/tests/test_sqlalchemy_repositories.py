import pytest
from sqlalchemy import delete, func, select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from ticket_api.database import create_session_factory
from ticket_api.models import (
    NewTicket,
    Ticket,
    TicketPriority,
    TicketStatus,
)
from ticket_api.persistence_models import TicketRecord
from ticket_api.sqlalchemy_repositories import (
    SqlAlchemyTicketRepository,
)

pytestmark = pytest.mark.integration


def assert_ticket_table_is_empty(engine: Engine) -> None:
    with engine.connect() as connection:
        ticket_count = connection.scalar(select(func.count()).select_from(TicketRecord))

    assert ticket_count == 0


def test_committed_ticket_is_visible_in_new_session(
    postgresql_test_engine: Engine,
) -> None:
    assert_ticket_table_is_empty(postgresql_test_engine)

    session_factory = create_session_factory(postgresql_test_engine)
    ticket_id: int | None = None

    try:
        with session_factory() as write_session:
            repository = SqlAlchemyTicketRepository(write_session)
            created_ticket = repository.create(
                NewTicket(
                    title="Committed database ticket",
                    priority=TicketPriority.HIGH,
                )
            )
            ticket_id = created_ticket.ticket_id

            write_session.commit()

        with session_factory() as read_session:
            repository = SqlAlchemyTicketRepository(read_session)
            stored_ticket = repository.get_by_id(ticket_id)

            assert stored_ticket == created_ticket
    finally:
        if ticket_id is not None:
            with postgresql_test_engine.begin() as connection:
                connection.execute(
                    delete(TicketRecord).where(TicketRecord.ticket_id == ticket_id)
                )


def test_rolled_back_ticket_is_not_visible_in_new_session(
    postgresql_test_engine: Engine,
) -> None:
    assert_ticket_table_is_empty(postgresql_test_engine)

    session_factory = create_session_factory(postgresql_test_engine)

    with session_factory() as write_session:
        repository = SqlAlchemyTicketRepository(write_session)
        created_ticket = repository.create(
            NewTicket(
                title="Rolled back database ticket",
                priority=TicketPriority.LOW,
            )
        )

        write_session.rollback()

    with session_factory() as read_session:
        repository = SqlAlchemyTicketRepository(read_session)

        assert repository.get_by_id(created_ticket.ticket_id) is None


def test_repository_update_advances_updated_at(
    postgresql_test_engine: Engine,
) -> None:
    assert_ticket_table_is_empty(postgresql_test_engine)

    session_factory = create_session_factory(postgresql_test_engine)
    ticket_id: int | None = None

    try:
        with session_factory() as create_session:
            repository = SqlAlchemyTicketRepository(create_session)
            ticket = repository.create(
                NewTicket(
                    title="Timestamp integration ticket",
                    priority=TicketPriority.MEDIUM,
                )
            )
            ticket_id = ticket.ticket_id
            create_session.commit()

        with session_factory() as update_session:
            repository = SqlAlchemyTicketRepository(update_session)
            stored_ticket = repository.get_by_id(ticket_id)

            assert stored_ticket is not None

            stored_ticket.change_title("Updated timestamp integration ticket")

            assert repository.update(stored_ticket) is True

            update_session.commit()

        with session_factory() as verification_session:
            record = verification_session.get(TicketRecord, ticket_id)

            assert record is not None
            assert record.updated_at > record.created_at
    finally:
        if ticket_id is not None:
            with postgresql_test_engine.begin() as connection:
                connection.execute(
                    delete(TicketRecord).where(TicketRecord.ticket_id == ticket_id)
                )


def test_repository_creates_database_generated_ticket(
    database_session: Session,
) -> None:
    repository = SqlAlchemyTicketRepository(database_session)

    ticket = repository.create(
        NewTicket(
            title="  Database integration ticket  ",
            priority=TicketPriority.HIGH,
        )
    )

    assert ticket.ticket_id > 0
    assert ticket.title == "Database integration ticket"
    assert ticket.priority is TicketPriority.HIGH
    assert ticket.status is TicketStatus.OPEN
    assert database_session.in_transaction() is True


def test_repository_gets_existing_ticket(database_session: Session) -> None:
    repository = SqlAlchemyTicketRepository(database_session)
    ticket = repository.create(
        NewTicket(
            title="Existing database ticket",
            priority=TicketPriority.MEDIUM,
        )
    )

    fetched_ticket = repository.get_by_id(ticket.ticket_id)

    assert fetched_ticket == ticket


def test_repository_returns_none_for_missing_ticket(database_session: Session) -> None:
    repository = SqlAlchemyTicketRepository(database_session)

    fetched_ticket = repository.get_by_id(9_000_000_000)

    assert fetched_ticket is None


def test_repository_lists_all_tickets_in_id_order(database_session: Session) -> None:
    repository = SqlAlchemyTicketRepository(database_session)
    first_ticket = repository.create(
        NewTicket(title="First ticket", priority=TicketPriority.LOW)
    )
    second_ticket = repository.create(
        NewTicket(title="Second ticket", priority=TicketPriority.HIGH)
    )

    tickets = repository.list_all()

    assert tickets == [first_ticket, second_ticket]


def test_repository_updates_ticket(database_session: Session) -> None:
    repository = SqlAlchemyTicketRepository(database_session)
    ticket = repository.create(
        NewTicket(
            title="Initial database ticket",
            priority=TicketPriority.LOW,
        )
    )

    ticket.change_title("Updated database ticket")
    ticket.change_priority(TicketPriority.CRITICAL)
    ticket.change_status(TicketStatus.RESOLVED)

    assert repository.update(ticket) is True

    database_session.expire_all()
    stored_ticket = repository.get_by_id(ticket.ticket_id)

    assert stored_ticket == ticket


def test_repository_returns_false_when_updating_missing_ticket(
    database_session: Session,
) -> None:
    repository = SqlAlchemyTicketRepository(database_session)
    missing_ticket = Ticket(
        ticket_id=9_000_000_000,
        title="Missing database ticket",
        priority=TicketPriority.LOW,
    )

    assert repository.update(missing_ticket) is False


def test_repository_deletes_ticket(database_session: Session) -> None:
    repository = SqlAlchemyTicketRepository(database_session)
    ticket = repository.create(
        NewTicket(
            title="To be deleted ticket",
            priority=TicketPriority.LOW,
        )
    )

    assert repository.delete(ticket.ticket_id) is True
    assert repository.get_by_id(ticket.ticket_id) is None
    assert repository.delete(ticket.ticket_id) is False


def test_repository_does_not_commit_created_ticket(
    database_session: Session,
    postgresql_test_engine: Engine,
) -> None:
    repository = SqlAlchemyTicketRepository(database_session)

    ticket = repository.create(
        NewTicket(
            title="Uncommitted database ticket",
            priority=TicketPriority.LOW,
        )
    )

    with postgresql_test_engine.connect() as connection:
        visible_ticket_id = connection.scalar(
            select(TicketRecord.ticket_id).where(
                TicketRecord.ticket_id == ticket.ticket_id
            )
        )

    assert visible_ticket_id is None
