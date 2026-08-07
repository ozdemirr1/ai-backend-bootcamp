class Ticket:
    def __init__(self, ticket_id: int, title: str, status: str):
        self.ticket_id = ticket_id
        self.title = title
        self.status = status

    def get_summary(self) -> str:
        return f"Ticket {self.ticket_id}: {self.title} | Status: {self.status}"

    def change_status(self, new_status: str) -> None:
        self.status = new_status


def main() -> None:
    first_ticket = Ticket(
        ticket_id=1001, title="Password reset is not received", status="open"
    )
    second_ticket = Ticket(
        ticket_id=1002, title="VPN connection fails", status="in_progress"
    )

    print(first_ticket.get_summary())

    first_ticket.change_status("in_progress")

    print(first_ticket.get_summary())
    print(second_ticket.get_summary())


if __name__ == "__main__":
    main()
