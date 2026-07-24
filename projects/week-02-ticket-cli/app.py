import json
from pathlib import Path

ALLOWED_PRIORITIES = ("low", "medium", "high", "critical")

TICKETS_FILE_PATH = Path(__file__).parent / "data" / "tickets.json"


def load_tickets(tickets_file_path):
    try:
        with tickets_file_path.open("r", encoding="utf-8") as tickets_file:
            return json.load(tickets_file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("Ticket data file contains invalid JSON.")
        return None


def save_tickets(tickets_file_path, tickets):
    tickets_file_path.parent.mkdir(exist_ok=True)

    with tickets_file_path.open("w", encoding="utf-8") as tickets_file:
        json.dump(tickets, tickets_file, indent=2, ensure_ascii=False)
        tickets_file.write("\n")


def is_valid_priority(priority):
    return priority in ALLOWED_PRIORITIES


def show_menu():
    print("\nOpsDesk Ticket CLI")
    print("1. List tickets")
    print("2. Add ticket")
    print("3. Exit")


def list_tickets(tickets):
    if not tickets:
        print("No tickets found.")
        return

    for ticket in tickets:
        print(
            f"[{ticket['id']}] {ticket['title']} | "
            f"Priority: {ticket['priority']} | "
            f"Status: {ticket['status']}"
        )


def add_ticket(tickets):
    title = input("Ticket title: ").strip()

    if not title:
        print("Ticket title cannot be empty.")
        return

    priority = input("Priority (low/medium/high/critical): ").strip().lower()
    if not is_valid_priority(priority):
        print("Invalid priority.")
        return

    new_ticket = {
        "id": len(tickets) + 1,
        "title": title,
        "priority": priority,
        "status": "open",
    }

    tickets.append(new_ticket)

    return new_ticket


def main():
    tickets = load_tickets(TICKETS_FILE_PATH)
    if tickets is None:
        return

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            list_tickets(tickets)
        elif choice == "2":
            new_ticket = add_ticket(tickets)
            if new_ticket is not None:
                save_tickets(TICKETS_FILE_PATH, tickets)
                print(f"Ticket {new_ticket['id']} created.")
        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()