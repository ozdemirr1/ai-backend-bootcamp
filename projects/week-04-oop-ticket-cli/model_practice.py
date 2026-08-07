from models import Ticket, TicketPriority, TicketStatus


def main() -> None:
    priority = TicketPriority.HIGH
    status = TicketStatus.IN_PROGRESS

    print(f"Priority Name: {priority.name}")
    print(f"Priority Value: {priority.value}")
    print(f"Status Name: {status.name}")
    print(f"Status Value: {status.value}")

    first_ticket = Ticket(
        ticket_id=1001,
        title="Password reset is not received",
        priority=TicketPriority.HIGH,
    )
    second_ticket = Ticket(
        ticket_id=1002,
        title="VPN connection fails",
        priority=TicketPriority.MEDIUM,
        status=TicketStatus.IN_PROGRESS,
    )

    print(first_ticket.get_summary())
    print(second_ticket.get_summary())
    print(first_ticket)


if __name__ == "__main__":
    main()
