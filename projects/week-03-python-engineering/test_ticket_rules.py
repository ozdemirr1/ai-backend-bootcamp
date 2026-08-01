import pytest

from ticket_rules import normalize_priorities, validate_priority


def test_normalize_priorities_cleans_values() -> None:
    raw_priorities = [" HIGH ", "medium", "CRITICAL"]

    result = normalize_priorities(raw_priorities)

    assert result == ["high", "medium", "critical"]


def test_validate_priority_rejects_unsupported_value() -> None:
    with pytest.raises(
        ValueError,
        match="Unsupported priority: archived",
    ):
        validate_priority("archived")


def test_validate_priority_normalizes_valid_value() -> None:
    result = validate_priority(" HIGH ")

    assert result == "high"
