from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

import jwt
import pytest

from ticket_api.clock import SystemClock
from ticket_api.tokens import InvalidAccessTokenError, JwtAccessTokenManager

FROZEN_TIME = datetime.now(UTC).replace(microsecond=0)
TEST_SECRET = "synthetic-test-secret-with-at-least-32-characters"


@dataclass(frozen=True)
class FrozenClock:
    current_time: datetime

    def now(self) -> datetime:
        return self.current_time


def test_system_clock_returns_timezone_aware_utc() -> None:
    clock = SystemClock()
    now = clock.now()

    assert now.tzinfo is UTC


def test_create_access_token_has_correct_claims() -> None:
    clock = FrozenClock(FROZEN_TIME)
    lifetime = timedelta(minutes=15)
    manager = JwtAccessTokenManager(secret=TEST_SECRET, lifetime=lifetime, clock=clock)

    token = manager.create_access_token(user_id=42)
    payload = jwt.decode(token, TEST_SECRET, algorithms=["HS256"])

    assert payload["sub"] == "42"
    assert "iat" in payload
    assert "exp" in payload

    iat = datetime.fromtimestamp(payload["iat"], UTC)
    exp = datetime.fromtimestamp(payload["exp"], UTC)

    assert iat == FROZEN_TIME
    assert exp - iat == lifetime


def test_decode_access_token_returns_correct_user_id() -> None:
    manager = JwtAccessTokenManager(
        secret=TEST_SECRET,
        lifetime=timedelta(minutes=15),
        clock=FrozenClock(FROZEN_TIME),
    )

    token = manager.create_access_token(user_id=42)
    user_id = manager.decode_access_token(token)

    assert user_id == 42


def test_decode_access_token_rejects_tampered_token() -> None:
    manager = JwtAccessTokenManager(
        secret=TEST_SECRET,
        lifetime=timedelta(minutes=15),
        clock=FrozenClock(FROZEN_TIME),
    )

    token = manager.create_access_token(user_id=42)

    header, payload, signature = token.split(".")

    tampered_char = "A" if signature[0] != "A" else "B"
    tampered_signature = tampered_char + signature[1:]
    tampered_token = ".".join((header, payload, tampered_signature))

    with pytest.raises(InvalidAccessTokenError):
        manager.decode_access_token(tampered_token)


def test_decode_access_token_rejects_wrong_secret() -> None:
    clock = FrozenClock(FROZEN_TIME)
    manager1 = JwtAccessTokenManager(
        secret=TEST_SECRET, lifetime=timedelta(minutes=15), clock=clock
    )
    manager2 = JwtAccessTokenManager(
        secret="different-secret-for-decoding-attempt",
        lifetime=timedelta(minutes=15),
        clock=clock,
    )

    token = manager1.create_access_token(user_id=42)

    with pytest.raises(InvalidAccessTokenError):
        manager2.decode_access_token(token)


def test_decode_access_token_rejects_wrong_algorithm() -> None:
    clock = FrozenClock(FROZEN_TIME)
    payload = {
        "sub": "42",
        "iat": clock.now(),
        "exp": clock.now() + timedelta(minutes=15),
    }

    token = jwt.encode(payload, TEST_SECRET, algorithm="HS384")

    manager = JwtAccessTokenManager(
        secret=TEST_SECRET, lifetime=timedelta(minutes=15), clock=clock
    )

    with pytest.raises(InvalidAccessTokenError):
        manager.decode_access_token(token)


def test_decode_access_token_rejects_expired_token() -> None:
    past_clock = FrozenClock(datetime(2020, 1, 1, tzinfo=UTC))
    manager = JwtAccessTokenManager(
        secret=TEST_SECRET, lifetime=timedelta(minutes=1), clock=past_clock
    )

    token = manager.create_access_token(user_id=42)

    with pytest.raises(InvalidAccessTokenError):
        manager.decode_access_token(token)


@pytest.mark.parametrize("missing_claim", ["sub", "iat", "exp"])
def test_decode_access_token_rejects_missing_claims(missing_claim: str) -> None:
    payload = {
        "sub": "42",
        "iat": FROZEN_TIME,
        "exp": FROZEN_TIME + timedelta(minutes=15),
    }

    del payload[missing_claim]

    token = jwt.encode(payload, TEST_SECRET, algorithm="HS256")
    manager = JwtAccessTokenManager(
        secret=TEST_SECRET,
        lifetime=timedelta(minutes=15),
        clock=FrozenClock(FROZEN_TIME),
    )

    with pytest.raises(InvalidAccessTokenError):
        manager.decode_access_token(token)


@pytest.mark.parametrize("invalid_sub", ["not-a-number", "-5", "0"])
def test_decode_access_token_rejects_invalid_sub(invalid_sub: str) -> None:
    payload = {
        "sub": invalid_sub,
        "iat": FROZEN_TIME,
        "exp": FROZEN_TIME + timedelta(minutes=15),
    }

    token = jwt.encode(payload, TEST_SECRET, algorithm="HS256")
    manager = JwtAccessTokenManager(
        secret=TEST_SECRET,
        lifetime=timedelta(minutes=15),
        clock=FrozenClock(FROZEN_TIME),
    )

    with pytest.raises(InvalidAccessTokenError):
        manager.decode_access_token(token)


def test_create_access_token_rejects_naive_clock() -> None:
    naive_clock = FrozenClock(datetime(2026, 9, 3, 12, 0))
    manager = JwtAccessTokenManager(
        secret=TEST_SECRET, lifetime=timedelta(minutes=15), clock=naive_clock
    )

    with pytest.raises(ValueError, match="timezone-aware datetime"):
        manager.create_access_token(user_id=42)


@pytest.mark.parametrize("invalid_user_id", [0, -1, "42"])
def test_create_access_token_rejects_invalid_user_id(invalid_user_id: int) -> None:
    manager = JwtAccessTokenManager(
        secret=TEST_SECRET,
        lifetime=timedelta(minutes=15),
        clock=FrozenClock(FROZEN_TIME),
    )

    with pytest.raises((TypeError, ValueError)):
        manager.create_access_token(user_id=invalid_user_id)  # type: ignore[arg-type]
