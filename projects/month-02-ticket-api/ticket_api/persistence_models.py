from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Boolean,
    CheckConstraint,
    DateTime,
    Identity,
    Index,
    Text,
    UniqueConstraint,
    func,
    text,
    true,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TicketRecord(Base):
    __tablename__ = "tickets"

    ticket_id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
    title: Mapped[str] = mapped_column(Text, nullable=False)
    priority: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        server_default=text("'open'"),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
    __table_args__ = (
        Index(
            "tickets_status_ticket_id_idx",
            "status",
            "ticket_id",
        ),
        CheckConstraint(
            "title = btrim(title) AND char_length(title) BETWEEN 3 AND 100",
            name="tickets_title_format",
        ),
        CheckConstraint(
            "priority IN ('low', 'medium', 'high', 'critical')",
            name="tickets_priority_allowed",
        ),
        CheckConstraint(
            "status IN ('open', 'in_progress', 'resolved', 'closed')",
            name="tickets_status_allowed",
        ),
        CheckConstraint("updated_at >= created_at", name="tickets_timestamp_order"),
    )


class UserRecord(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(always=True),
        primary_key=True,
    )
    email: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    password_hash: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )
    role: Mapped[str] = mapped_column(
        Text,
        nullable=False,
        server_default=text("'member'"),
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=true(),
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )

    __table_args__ = (
        UniqueConstraint(
            "email",
            name="users_email_key",
        ),
        CheckConstraint(
            "email = btrim(email) AND email = lower(email) "
            "AND char_length(email) BETWEEN 3 AND 254",
            name="users_email_format",
        ),
        CheckConstraint(
            "role IN ('member', 'admin')",
            name="users_role_allowed",
        ),
        CheckConstraint(
            "updated_at >= created_at",
            name="users_timestamp_order",
        ),
    )
