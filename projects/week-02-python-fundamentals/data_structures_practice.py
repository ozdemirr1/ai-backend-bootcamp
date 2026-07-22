ticket_statuses = ["open", "in_progress", "resolved"]

print(f"First status: {ticket_statuses[0]}")
print(f"Last status: {ticket_statuses[-1]}")

ticket_statuses.append("waiting_for_customer")

print(f"Status count: {len(ticket_statuses)}")

for status in ticket_statuses:
    print(f"Ticket status: {status}")

ticket = {
    "id": 1001,
    "title": "Password reset email is not received",
    "priority": "high",
    "is_resolved": False,
}

print(f"Ticket title: {ticket['title']}")

ticket["is_resolved"] = True
ticket["assigned_user"] = "Furkan"

print(f"Resolved: {ticket['is_resolved']}")
print(f"Assigned user: {ticket['assigned_user']}")

second_ticket = {
    "id": 1002,
    "title": "VPN connection fails",
    "priority": "medium",
    "is_resolved": False,
    "assigned_user": None,
}

tickets = [ticket, second_ticket]

for ticket_item in tickets:
    print(f"Ticket {ticket_item['id']}: {ticket_item['title']}")

unresolved_ticket_count = 0

for ticket_item in tickets:
    if not ticket_item["is_resolved"]:
        unresolved_ticket_count += 1

print(f"Unresolved ticket count: {unresolved_ticket_count}")

supported_priorities = ("critical", "high", "medium", "low")

print(f"First supported priority: {supported_priorities[0]}")
print(f"Supported priority count: {len(supported_priorities)}")
print(f"Supports high priority: {'high' in supported_priorities}")

raw_ticket_tags = ["authentication", "email", "authentication", "urgent"]
unique_ticket_tags = set(raw_ticket_tags)

print(f"Unique tag count: {len(unique_ticket_tags)}")
print(f"Has urgent tag: {'urgent' in unique_ticket_tags}")

assert ticket_statuses[-1] == "waiting_for_customer"
assert ticket["assigned_user"] == "Furkan"
assert len(tickets) == 2
assert unresolved_ticket_count == 1
assert "critical" in supported_priorities
assert len(unique_ticket_tags) == 3
assert "urgent" in unique_ticket_tags

print("All data structure checks passed.")