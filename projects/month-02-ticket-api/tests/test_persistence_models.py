from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    UniqueConstraint,
)

from ticket_api.persistence_models import Base, TicketRecord, UserRecord


def test_ticket_record_uses_expected_table_and_columns() -> None:
    table = TicketRecord.__table__

    assert table.name == "tickets"
    assert list(table.columns.keys()) == [
        "ticket_id",
        "owner_id",
        "title",
        "priority",
        "status",
        "created_at",
        "updated_at",
    ]
    assert Base.metadata.tables["tickets"] is table


def test_ticket_record_uses_database_generated_identity() -> None:
    column = TicketRecord.__table__.c.ticket_id

    assert column.primary_key is True
    assert isinstance(column.type, BigInteger)
    assert column.identity is not None
    assert column.identity.always is True
    assert column.nullable is False


def test_ticket_record_uses_expected_defaults_and_timestamps() -> None:
    table = TicketRecord.__table__

    status = table.c.status
    assert status.server_default is not None
    assert str(status.server_default.arg) == "'open'"
    assert status.nullable is False

    created_at = table.c.created_at
    assert isinstance(created_at.type, DateTime)
    assert created_at.type.timezone is True
    assert created_at.server_default is not None
    assert created_at.nullable is False

    updated_at = table.c.updated_at
    assert isinstance(updated_at.type, DateTime)
    assert updated_at.type.timezone is True
    assert updated_at.server_default is not None
    assert updated_at.nullable is False
    assert updated_at.onupdate is not None
    assert "CURRENT_TIMESTAMP" in str(updated_at.onupdate.arg)

    assert table.c.title.nullable is False
    assert table.c.priority.nullable is False


def test_ticket_record_declares_expected_check_constraints() -> None:
    check_constraints = {
        constraint.name: str(constraint.sqltext)
        for constraint in TicketRecord.__table__.constraints
        if isinstance(constraint, CheckConstraint)
    }

    expected_constraints = {
        "tickets_title_format",
        "tickets_priority_allowed",
        "tickets_status_allowed",
        "tickets_timestamp_order",
    }

    assert set(check_constraints.keys()) == expected_constraints


def test_ticket_record_declares_status_listing_index() -> None:
    indexes = {
        index.name: [column.name for column in index.columns]
        for index in TicketRecord.__table__.indexes
    }

    assert indexes == {
        "tickets_status_ticket_id_idx": [
            "status",
            "ticket_id",
        ],
        "tickets_owner_id_status_ticket_id_idx": [
            "owner_id",
            "status",
            "ticket_id",
        ],
    }


def test_user_record_uses_expected_table_and_columns() -> None:
    table = UserRecord.__table__

    assert table.name == "users"
    assert list(table.columns.keys()) == [
        "user_id",
        "email",
        "password_hash",
        "role",
        "is_active",
        "created_at",
        "updated_at",
    ]
    assert Base.metadata.tables["users"] is table


def test_user_record_uses_database_generated_identity() -> None:
    column = UserRecord.__table__.columns["user_id"]

    assert column.primary_key is True
    assert isinstance(column.type, BigInteger)
    assert column.identity is not None
    assert column.identity.always is True


def test_user_record_declares_unique_email() -> None:
    unique_constraints = {
        constraint.name: [column.name for column in constraint.columns]
        for constraint in UserRecord.__table__.constraints
        if isinstance(constraint, UniqueConstraint)
    }

    assert unique_constraints == {
        "users_email_key": ["email"],
    }


def test_user_record_uses_safe_defaults_and_timestamps() -> None:
    columns = UserRecord.__table__.columns

    assert columns["email"].nullable is False
    assert columns["password_hash"].nullable is False

    assert columns["role"].nullable is False
    assert columns["role"].server_default is not None

    assert columns["is_active"].nullable is False
    assert isinstance(columns["is_active"].type, Boolean)
    assert columns["is_active"].server_default is not None

    created_col = columns["created_at"]
    assert isinstance(created_col.type, DateTime)
    assert created_col.type.timezone is True
    assert created_col.server_default is not None

    updated_col = columns["updated_at"]
    assert isinstance(updated_col.type, DateTime)
    assert updated_col.type.timezone is True
    assert updated_col.server_default is not None
    assert updated_col.onupdate is not None


def test_user_record_declares_expected_check_constraints() -> None:
    check_constraints = {
        constraint.name
        for constraint in UserRecord.__table__.constraints
        if isinstance(constraint, CheckConstraint)
    }

    assert check_constraints == {
        "users_email_format",
        "users_role_allowed",
        "users_timestamp_order",
    }


def test_ticket_record_declares_nullable_owner_foreign_key() -> None:
    column = TicketRecord.__table__.c.owner_id

    assert isinstance(column.type, BigInteger)
    assert column.nullable is True

    foreign_key = next(iter(column.foreign_keys))

    assert foreign_key.target_fullname == "users.user_id"
    assert foreign_key.ondelete == "RESTRICT"
    assert foreign_key.constraint.name == "tickets_owner_id_fkey"
