from pathlib import Path
from tempfile import TemporaryDirectory

from app import is_valid_priority, load_tickets, save_tickets


def test_priority_validation():
    assert is_valid_priority("high")
    assert not is_valid_priority("urgent")


def test_ticket_persistence():
    sample_tickets = [
        {
            "id": 1,
            "title": "Test ticket",
            "priority": "high",
            "status": "open",
        },
    ]

    with TemporaryDirectory() as temporary_directory:
        tickets_file_path = Path(temporary_directory) / "tickets.json"

        assert load_tickets(tickets_file_path) == []

        save_tickets(tickets_file_path, sample_tickets)
        loaded_tickets = load_tickets(tickets_file_path)

    assert loaded_tickets == sample_tickets


if __name__ == "__main__":
    test_priority_validation()
    test_ticket_persistence()
    print("All CLI checks passed.")