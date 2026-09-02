from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from ticket_api.dependencies import get_registration_service
from ticket_api.main import create_app
from ticket_api.repositories import InMemoryUserRepository
from ticket_api.services import RegistrationService


class SyntheticPasswordHasher:
    def hash_password(self, plain_password: str) -> str:
        return "$argon2id$synthetic-api-test-hash"


@pytest.fixture
def auth_client() -> Iterator[TestClient]:
    application = create_app(lifespan_handler=None)
    repository = InMemoryUserRepository()
    service = RegistrationService(
        repository=repository,
        password_hasher=SyntheticPasswordHasher(),
    )

    def get_test_registration_service() -> RegistrationService:
        return service

    application.dependency_overrides[get_registration_service] = (
        get_test_registration_service
    )

    try:
        with TestClient(application) as client:
            yield client
    finally:
        application.dependency_overrides.pop(get_registration_service, None)


def test_register_valid_user_returns_201(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/auth/register",
        json={"email": "furkan@example.com", "password": "my_secret_password_123"},
    )

    assert response.status_code == 201


def test_register_response_contains_only_expected_fields(
    auth_client: TestClient,
) -> None:
    response = auth_client.post(
        "/auth/register",
        json={"email": "furkan@example.com", "password": "my_secret_password_123"},
    )

    data = response.json()
    assert set(data.keys()) == {"user_id", "email", "role", "is_active"}


def test_register_response_normalizes_email(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/auth/register",
        json={"email": " FURKAN@Example.COM ", "password": "my_secret_password_123"},
    )

    assert response.json()["email"] == "furkan@example.com"


def test_register_response_excludes_password_fields(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/auth/register",
        json={"email": "furkan@example.com", "password": "my_secret_password_123"},
    )

    data = response.json()
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email_returns_409(auth_client: TestClient) -> None:
    payload = {"email": "furkan@example.com", "password": "my_secret_password_123"}

    auth_client.post("/auth/register", json=payload)
    response = auth_client.post("/auth/register", json=payload)

    assert response.status_code == 409


def test_register_short_password_returns_422(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/auth/register",
        json={"email": "furkan@example.com", "password": "short"},
    )

    assert response.status_code == 422


def test_register_with_extra_role_field_returns_422(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/auth/register",
        json={
            "email": "furkan@example.com",
            "password": "my_secret_password_123",
            "role": "admin",
        },
    )

    assert response.status_code == 422
