import pytest
from pydantic import ValidationError

from ticket_api.schemas import TicketUpdateRequest


def test_ticket_update_accepts_and_strips_title() -> None:
    update = TicketUpdateRequest(title="  Update Network Issue  ")

    assert update.title == "Update Network Issue"
    assert update.priority is None
    assert update.status is None


def test_ticket_update_accepts_single_priority() -> None:
    update = TicketUpdateRequest(priority="high")

    assert update.priority == "high"
    assert update.title is None
    assert update.status is None


def test_ticket_update_accepts_single_status() -> None:
    update = TicketUpdateRequest(status="in_progress")

    assert update.status == "in_progress"
    assert update.title is None
    assert update.priority is None


def test_ticket_update_accepts_multiple_fields() -> None:
    update = TicketUpdateRequest(
        title="Updated Title",
        status="resolved",
    )

    assert update.title == "Updated Title"
    assert update.status == "resolved"
    assert update.priority is None


def test_ticket_update_rejects_empty_body() -> None:
    with pytest.raises(ValidationError, match="at least one field"):
        TicketUpdateRequest()


def test_ticket_update_rejects_all_none_fields() -> None:
    with pytest.raises(ValidationError, match="at least one field"):
        TicketUpdateRequest(title=None, priority=None, status=None)


def test_ticket_update_rejects_invalid_status() -> None:
    with pytest.raises(ValidationError, match="status"):
        TicketUpdateRequest(status="unknown_status")


def test_ticket_update_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError, match="extra_field"):
        TicketUpdateRequest(
            title="Valid Title",
            extra_field="not allowed",
        )


def test_ticket_update_model_dump_excludes_none() -> None:
    update = TicketUpdateRequest(priority="critical")

    assert update.model_dump(exclude_none=True) == {
        "priority": "critical",
    }
