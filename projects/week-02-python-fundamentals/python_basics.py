ticket_id = 1001
title = "Password reset email is not received"
description = "User cannot receive the password reset email."
priority = "high"
estimated_hours = 1.5
is_resolved = False
assigned_user = None

print(f"Ticket ID: {ticket_id}, type: {type(ticket_id)}")
print(f"Title: {title}, type: {type(title)}")
print(f"Description: {description}, type: {type(description)}")
print(f"Priority: {priority}, type: {type(priority)}")
print(f"Estimated Hours: {estimated_hours}, type: {type(estimated_hours)}")
print(f"Is Resolved: {is_resolved}, type: {type(is_resolved)}")
print(f"Assigned User: {assigned_user}, type: {type(assigned_user)}")

sla_hours = 0

if priority == "critical":
    sla_hours = 1
elif priority == "high":
    sla_hours = 4
elif priority == "medium":
    sla_hours = 8
elif priority == "low":
    sla_hours = 24
else:
    print("Invalid priority.")

print(f"Priority: {priority}, SLA Hours: {sla_hours}")

if is_resolved:
    print("The ticket has been resolved.")
elif assigned_user is None:
    print("The ticket is waiting to be assigned to a user.")
else:
    print(f"The ticket is in progress and assigned to {assigned_user}.")

ticket_priorities = ["critical", "high", "medium", "low"]

for ticket_priority in ticket_priorities:
    print(f"Ticket priority: {ticket_priority}")


urgent_ticket_count = 0

for ticket_priority in ticket_priorities:
    if ticket_priority == "critical" or ticket_priority == "high":
        urgent_ticket_count += 1

print(f"Number of critical and high priority tickets: {urgent_ticket_count}")

remaining_tickets = 3

while remaining_tickets > 0:
    print(f"Remaining tickets: {remaining_tickets}")
    remaining_tickets -= 1

print("All tickets have been processed.")