from typing import Optional

from ticket_rules import (
    SLA_HOURS_BY_PRIORITY,
    get_sla_hours,
    is_urgent_priority,
    normalize_priorities,
    validate_priority,
)


def get_assignee_label(assigned_user: Optional[str]) -> str:
    if assigned_user is None:
        return "Unassigned"

    return assigned_user


def main() -> None:
    raw_priorities = [" HIGH ", "medium", "CRITICAL", "low "]
    normalized_priorities = normalize_priorities(raw_priorities)
    urgent_priorities = [
        priority for priority in normalized_priorities if is_urgent_priority(priority)
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

    try:
        validated_priority = validate_priority(" HIGH ")
    except ValueError as error:
        print(f"Priority validation failed: {error}")
    else:
        print(f"Validated priority: {validated_priority}")
    finally:
        print("Priority validation finished.")


if __name__ == "__main__":
    main()
