from typing import Optional

from models import Ticket, TicketPriority
from repositories import TicketRepository
from services import TicketService


def show_menu() -> None:
    print("OpsDesk OOP Ticket CLI")
    print("1. List tickets")
    print("2. Add ticket")
    print("3. Exit")


def display_tickets(service: TicketService) -> None:
    tickets = service.list_tickets()
    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        print(ticket.get_summary())


def add_ticket(service: TicketService) -> Optional[Ticket]:
    ticket_id = int(input("Ticket ID: ").strip())
    title = input("Ticket title: ").strip()
    priority_input = input("Priority (low/medium/high/critical): ").strip().lower()

    try:
        priority = TicketPriority(priority_input)
    except ValueError:
        print("Invalid priority.")
        return None

    try:
        ticket = service.create_ticket(
            ticket_id=ticket_id,
            title=title,
            priority=priority,
        )
    except (TypeError, ValueError) as error:
        print(f"Ticket could not be created: {error}")
        return None

    print(f"Ticket {ticket.ticket_id} created.")
    return ticket


def run_cli(service: TicketService) -> None:
    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            display_tickets(service)
        elif choice == "2":
            add_ticket(service)
        elif choice == "3":
            print("Goodbye.")
            return
        else:
            print("Invalid option.")


def main() -> None:
    repository = TicketRepository()
    service = TicketService(repository)

    run_cli(service)


if __name__ == "__main__":
    main()
