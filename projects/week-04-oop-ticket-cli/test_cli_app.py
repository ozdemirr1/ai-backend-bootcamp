from models import TicketPriority, TicketStatus
from oop_ticket_cli import add_ticket, display_tickets, run_cli
from repositories import TicketRepository
from services import TicketService


def test_display_tickets_shows_empty_message(capsys) -> None:
    repository = TicketRepository()
    service = TicketService(repository)

    display_tickets(service)

    captured = capsys.readouterr()
    assert captured.out == "No tickets found.\n"


def test_display_tickets_shows_ticket_summaries(capsys) -> None:
    repository = TicketRepository()
    service = TicketService(repository)

    first_ticket = service.create_ticket(
        ticket_id=1, title="First Ticket", priority=TicketPriority.LOW
    )
    second_ticket = service.create_ticket(
        ticket_id=2, title="Second Ticket", priority=TicketPriority.HIGH
    )

    display_tickets(service)

    captured = capsys.readouterr()

    assert captured.out == (
        f"{first_ticket.get_summary()}\n{second_ticket.get_summary()}\n"
    )


def test_add_ticket_creates_ticket_from_user_input(monkeypatch, capsys) -> None:
    repository = TicketRepository()
    service = TicketService(repository)

    answers = iter(["1001", "Printer is offline", "HIGH"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    created_ticket = add_ticket(service)

    captured = capsys.readouterr()

    assert created_ticket.ticket_id == 1001
    assert created_ticket.title == "Printer is offline"
    assert created_ticket.priority == TicketPriority.HIGH
    assert created_ticket.status == TicketStatus.OPEN
    assert repository.list_all() == [created_ticket]
    assert captured.out == f"Ticket {created_ticket.ticket_id} created.\n"


def test_add_ticket_rejects_invalid_priority(monkeypatch, capsys) -> None:
    repository = TicketRepository()
    service = TicketService(repository)

    answers = iter(["1002", "VPN connection fails", "urgent"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    result = add_ticket(service)

    captured = capsys.readouterr()

    assert result is None
    assert repository.list_all() == []
    assert captured.out == "Invalid priority.\n"


def test_add_ticket_rejects_empty_title(monkeypatch, capsys) -> None:
    repository = TicketRepository()
    service = TicketService(repository)

    answers = iter(["1003", "   ", "high"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    result = add_ticket(service)

    captured = capsys.readouterr()

    assert result is None
    assert repository.list_all() == []
    assert captured.out == ("Ticket could not be created: title cannot be empty\n")


def test_run_cli_handles_invalid_option_and_exit(monkeypatch, capsys) -> None:
    repository = TicketRepository()
    service = TicketService(repository)

    answers = iter(["9", "3"])
    monkeypatch.setattr("builtins.input", lambda _: next(answers))

    run_cli(service)

    captured = capsys.readouterr()

    assert "Invalid option.\n" in captured.out
    assert captured.out.endswith("Goodbye.\n")
    assert captured.out.count("OpsDesk OOP Ticket CLI") == 2
