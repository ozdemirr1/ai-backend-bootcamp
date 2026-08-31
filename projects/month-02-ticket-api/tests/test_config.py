import pytest
from pydantic import ValidationError

from ticket_api.config import Settings


@pytest.fixture(autouse=True)
def valid_settings_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("DATABASE_URL", "postgresql+psycopg://example")
    monkeypatch.setenv(
        "JWT_SECRET",
        "test-jwt-secret-with-at-least-32-characters",
    )
    monkeypatch.delenv("ACCESS_TOKEN_EXPIRE_MINUTES", raising=False)


def test_settings_reads_database_url_from_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database_url = "postgresql+psycopg://another-example"

    monkeypatch.setenv("DATABASE_URL", database_url)

    settings = Settings(_env_file=None)

    assert settings.database_url.get_secret_value() == database_url


def test_settings_rejects_missing_database_url(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("DATABASE_URL", raising=False)

    with pytest.raises(ValidationError, match="database_url"):
        Settings(_env_file=None)


def test_settings_hides_database_url_in_representation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    database_url = "postgresql+psycopg://another-example"

    monkeypatch.setenv("DATABASE_URL", database_url)

    settings = Settings(_env_file=None)

    assert database_url not in repr(settings)
    assert "**********" in repr(settings)


def test_settings_reads_jwt_secret_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    jwt_secret = "another-test-jwt-secret-with-32-characters"
    monkeypatch.setenv("JWT_SECRET", jwt_secret)

    settings = Settings(_env_file=None)

    assert settings.jwt_secret.get_secret_value() == jwt_secret


def test_settings_raises_validation_error_when_jwt_secret_is_missing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("JWT_SECRET", raising=False)

    with pytest.raises(ValidationError, match="jwt_secret"):
        Settings(_env_file=None)


def test_settings_rejects_jwt_secret_shorter_than_32_characters(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("JWT_SECRET", "short_secret")

    with pytest.raises(ValidationError, match="jwt_secret"):
        Settings(_env_file=None)


def test_settings_hides_jwt_secret_in_representation(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    jwt_secret = "s" * 32
    monkeypatch.setenv("JWT_SECRET", jwt_secret)

    settings = Settings(_env_file=None)
    representation = repr(settings)

    assert jwt_secret not in representation
    assert "**********" in representation


def test_settings_has_default_token_expiration_of_30_minutes(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    settings = Settings(_env_file=None)

    assert settings.access_token_expire_minutes == 30


@pytest.mark.parametrize("invalid_expiration", ["0", "1441"])
def test_settings_rejects_out_of_bounds_token_expiration(
    monkeypatch: pytest.MonkeyPatch,
    invalid_expiration: str,
) -> None:
    monkeypatch.setenv("ACCESS_TOKEN_EXPIRE_MINUTES", invalid_expiration)

    with pytest.raises(ValidationError, match="access_token_expire_minutes"):
        Settings(_env_file=None)
