def show_opsdesk_status():
    print("OpsDesk support system is ready.")


def show_ticket_details(ticket_title, ticket_priority):
    print(f"Ticket title: {ticket_title}")
    print(f"Ticket priority: {ticket_priority}")


def calculate_sla_hours(ticket_priority):
    if ticket_priority == "critical":
        return 1
    elif ticket_priority == "high":
        return 4
    elif ticket_priority == "medium":
        return 8
    elif ticket_priority == "low":
        return 24
    else:
        return None


show_opsdesk_status()
show_ticket_details("Password reset email is not received", "high")

sla_hours = calculate_sla_hours("high")
print(f"SLA hours: {sla_hours}")

assert calculate_sla_hours("critical") == 1
assert calculate_sla_hours("high") == 4
assert calculate_sla_hours("medium") == 8
assert calculate_sla_hours("low") == 24
assert calculate_sla_hours("unknown") is None

print("All SLA checks passed.")