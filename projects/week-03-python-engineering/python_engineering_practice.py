from typing import Optional

SLA_HOURS_BY_PRIORITY: dict[str, int] = {
    "critical": 1,
    "high": 4,
    "medium": 8,
    "low": 24,
}


def normalize_priorities(raw_priorities: list[str]) -> list[str]:
    return [priority.strip().lower() for priority in raw_priorities]


def is_urgent_priority(priority: str) -> bool:
    return priority in ("high", "critical")


def get_assignee_label(assigned_user: Optional[str]) -> str:
    if assigned_user is None:
        return "Unassigned"

    return assigned_user


def get_sla_hours(
    priority: str,
    sla_hours_by_priority: dict[str, int],
) -> Optional[int]:
    return sla_hours_by_priority.get(priority)


raw_priorities = [" HIGH ", "medium", "CRITICAL", "low "]
normalized_priorities = normalize_priorities(raw_priorities)
urgent_priorities = [
    priority
    for priority in normalized_priorities
    if is_urgent_priority(priority)
]
unassigned_label = get_assignee_label(None)
assigned_label = get_assignee_label("Furkan")
high_sla_hours = get_sla_hours("high", SLA_HOURS_BY_PRIORITY)
unknown_sla_hours = get_sla_hours("unknown", SLA_HOURS_BY_PRIORITY)

print(f"Normalized priorities: {normalized_priorities}")
print(f"Urgent priorities: {urgent_priorities}")
print(f"Unassigned ticket label: {unassigned_label}")
print(f"Assigned ticket label: {assigned_label}")
print(f"High SLA hours: {high_sla_hours}")
print(f"Unknown SLA hours: {unknown_sla_hours}")