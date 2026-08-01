from pathlib import Path

from app import is_valid_priority, load_tickets, save_tickets


def test_priority_validation() -> None:
    assert is_valid_priority("high")
    assert not is_valid_priority("urgent")


def test_ticket_persistence(tmp_path: Path) -> None:
    sample_tickets = [
        {
            "id": 1,
            "title": "Test ticket",
            "priority": "high",
            "status": "open",
        },
    ]

    tickets_file_path = tmp_path / "tickets.json"

    assert load_tickets(tickets_file_path) == []

    save_tickets(tickets_file_path, sample_tickets)
    loaded_tickets = load_tickets(tickets_file_path)

    assert loaded_tickets == sample_tickets


def test_load_tickets_returns_none_for_invalid_json(
    tmp_path: Path,
) -> None:
    tickets_file_path = tmp_path / "tickets.json"

    tickets_file_path.write_text("{invalid", encoding="utf-8")

    result = load_tickets(tickets_file_path)

    assert result is None
