from typing import Optional

SLA_HOURS_BY_PRIORITY: dict[str, int] = {
    "critical": 1,
    "high": 4,
    "medium": 8,
    "low": 24,
}


def validate_priority(priority: str) -> str:
    normalized_priority = priority.strip().lower()

    if normalized_priority not in SLA_HOURS_BY_PRIORITY:
        raise ValueError(f"Unsupported priority: {priority}")

    return normalized_priority


def normalize_priorities(raw_priorities: list[str]) -> list[str]:
    return [priority.strip().lower() for priority in raw_priorities]


def is_urgent_priority(priority: str) -> bool:
    return priority in ("high", "critical")


def get_sla_hours(
    priority: str,
    sla_hours_by_priority: dict[str, int],
) -> Optional[int]:
    return sla_hours_by_priority.get(priority)
