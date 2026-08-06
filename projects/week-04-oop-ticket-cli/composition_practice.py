class MessageFormatter:
    def format(self, ticket_title: str) -> str:
        return f"New ticket: {ticket_title}"


class TicketNotificationService:
    def __init__(self, formatter: MessageFormatter) -> None:
        self._formatter = formatter

    def create_notification(self, ticket_title: str) -> str:
        message = self._formatter.format(ticket_title)
        return message


def main() -> None:
    formatter = MessageFormatter()
    notification_service = TicketNotificationService(formatter)
    notification = notification_service.create_notification("Password reset problem")
    print(notification)


if __name__ == "__main__":
    main()
