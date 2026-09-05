from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient

from ticket_api.dependencies import (
    get_authentication_service,
    get_current_user_service,
    get_registration_service,
    get_ticket_service,
)
from ticket_api.main import create_app
from ticket_api.repositories import (
    InMemoryTicketRepository,
    InMemoryUserRepository,
)
from ticket_api.services import (
    AuthenticationService,
    CurrentUserService,
    RegistrationService,
    TicketService,
)
from ticket_api.tokens import InvalidAccessTokenError

VALID_PASSWORD = "my_secret_password_123"
SYNTHETIC_PASSWORD_HASH = "$argon2id$synthetic-api-test-hash"
SYNTHETIC_DUMMY_HASH = "$argon2id$synthetic-dummy-hash"


class SyntheticPasswordManager:
    def hash_password(self, plain_password: str) -> str:
        return SYNTHETIC_PASSWORD_HASH

    def verify_password(
        self,
        plain_password: str,
        password_hash: str,
    ) -> bool:
        return (
            plain_password == VALID_PASSWORD
            and password_hash == SYNTHETIC_PASSWORD_HASH
        )


class SyntheticTokenManager:
    def create_access_token(self, user_id: int) -> str:
        return f"synthetic-token-for-user-{user_id}"

    def decode_access_token(self, token: str) -> int:
        if token != "synthetic-token-for-user-1":
            raise InvalidAccessTokenError("Invalid access token")

        return 1


@pytest.fixture
def auth_client() -> Iterator[TestClient]:
    application = create_app(lifespan_handler=None)
    repository = InMemoryUserRepository()

    password_manager = SyntheticPasswordManager()

    token_manager = SyntheticTokenManager()

    ticket_service = TicketService(InMemoryTicketRepository())

    registration_service = RegistrationService(
        repository=repository,
        password_hasher=password_manager,
    )

    authentication_service = AuthenticationService(
        repository=repository,
        password_verifier=password_manager,
        token_issuer=token_manager,
        dummy_password_hash=SYNTHETIC_DUMMY_HASH,
    )

    current_user_service = CurrentUserService(
        repository=repository,
        token_decoder=token_manager,
    )

    def get_test_ticket_service() -> TicketService:
        return ticket_service

    def get_test_current_user_service() -> CurrentUserService:
        return current_user_service

    def get_test_registration_service() -> RegistrationService:
        return registration_service

    def get_test_authentication_service() -> AuthenticationService:
        return authentication_service

    application.dependency_overrides[get_registration_service] = (
        get_test_registration_service
    )
    application.dependency_overrides[get_authentication_service] = (
        get_test_authentication_service
    )
    application.dependency_overrides[get_current_user_service] = (
        get_test_current_user_service
    )
    application.dependency_overrides[get_ticket_service] = get_test_ticket_service

    try:
        with TestClient(application) as client:
            yield client
    finally:
        application.dependency_overrides.pop(
            get_registration_service,
            None,
        )
        application.dependency_overrides.pop(
            get_authentication_service,
            None,
        )
        application.dependency_overrides.pop(
            get_current_user_service,
            None,
        )
        application.dependency_overrides.pop(
            get_ticket_service,
            None,
        )


def test_register_valid_user_returns_201(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/auth/register",
        json={"email": "furkan@example.com", "password": VALID_PASSWORD},
    )

    assert response.status_code == 201


def test_register_response_contains_only_expected_fields(
    auth_client: TestClient,
) -> None:
    response = auth_client.post(
        "/auth/register",
        json={"email": "furkan@example.com", "password": VALID_PASSWORD},
    )

    data = response.json()
    assert set(data.keys()) == {"user_id", "email", "role", "is_active"}


def test_register_response_normalizes_email(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/auth/register",
        json={"email": " FURKAN@Example.COM ", "password": VALID_PASSWORD},
    )

    assert response.json()["email"] == "furkan@example.com"


def test_register_response_excludes_password_fields(auth_client: TestClient) -> None:
    response = auth_client.post(
        "/auth/register",
        json={"email": "furkan@example.com", "password": VALID_PASSWORD},
    )

    data = response.json()
    assert "password" not in data
    assert "password_hash" not in data


def test_register_duplicate_email_returns_409(auth_client: TestClient) -> None:
    payload = {"email": "furkan@example.com", "password": VALID_PASSWORD}

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
            "password": VALID_PASSWORD,
            "role": "admin",
        },
    )

    assert response.status_code == 422


def test_login_valid_credentials_returns_bearer_token(
    auth_client: TestClient,
) -> None:
    auth_client.post(
        "/auth/register",
        json={
            "email": "furkan@example.com",
            "password": VALID_PASSWORD,
        },
    )

    response = auth_client.post(
        "/auth/login",
        json={
            "email": "furkan@example.com",
            "password": VALID_PASSWORD,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "access_token": "synthetic-token-for-user-1",
        "token_type": "bearer",
    }


def test_login_wrong_password_and_missing_user_share_generic_401(
    auth_client: TestClient,
) -> None:
    auth_client.post(
        "/auth/register",
        json={
            "email": "furkan@example.com",
            "password": VALID_PASSWORD,
        },
    )

    wrong_password_response = auth_client.post(
        "/auth/login",
        json={
            "email": "furkan@example.com",
            "password": "wrong_password",
        },
    )
    missing_user_response = auth_client.post(
        "/auth/login",
        json={
            "email": "missing@example.com",
            "password": VALID_PASSWORD,
        },
    )

    expected_body = {"detail": "Invalid email or password"}

    assert wrong_password_response.status_code == 401
    assert missing_user_response.status_code == 401
    assert wrong_password_response.json() == expected_body
    assert missing_user_response.json() == expected_body
    assert wrong_password_response.headers["www-authenticate"] == "Bearer"
    assert missing_user_response.headers["www-authenticate"] == "Bearer"


def test_login_invalid_request_returns_422(
    auth_client: TestClient,
) -> None:
    response = auth_client.post(
        "/auth/login",
        json={
            "email": "not-an-email",
            "password": "",
        },
    )

    assert response.status_code == 422


def test_users_me_returns_authenticated_public_user(
    auth_client: TestClient,
) -> None:
    registration_response = auth_client.post(
        "/auth/register",
        json={
            "email": "furkan@example.com",
            "password": VALID_PASSWORD,
        },
    )
    assert registration_response.status_code == 201

    login_response = auth_client.post(
        "/auth/login",
        json={
            "email": "furkan@example.com",
            "password": VALID_PASSWORD,
        },
    )
    access_token = login_response.json()["access_token"]

    response = auth_client.get(
        "/users/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "user_id": 1,
        "email": "furkan@example.com",
        "role": "member",
        "is_active": True,
    }
    assert "password_hash" not in response.json()


def test_users_me_rejects_missing_authorization_header(
    auth_client: TestClient,
) -> None:
    response = auth_client.get("/users/me")

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authentication credentials"}
    assert response.headers["www-authenticate"] == "Bearer"


def test_users_me_rejects_wrong_authorization_scheme(
    auth_client: TestClient,
) -> None:
    response = auth_client.get(
        "/users/me",
        headers={
            "Authorization": "Basic synthetic-credentials",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authentication credentials"}
    assert response.headers["www-authenticate"] == "Bearer"


def test_users_me_rejects_invalid_bearer_token(
    auth_client: TestClient,
) -> None:
    response = auth_client.get(
        "/users/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authentication credentials"}
    assert response.headers["www-authenticate"] == "Bearer"


def test_create_ticket_rejects_missing_authorization_header(
    auth_client: TestClient,
) -> None:
    response = auth_client.post(
        "/tickets",
        json={
            "title": "Unauthenticated ticket",
            "priority": "high",
        },
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authentication credentials"}
    assert response.headers["www-authenticate"] == "Bearer"


def test_list_tickets_rejects_missing_authorization_header(
    auth_client: TestClient,
) -> None:
    response = auth_client.get("/tickets")

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid authentication credentials"}
    assert response.headers["www-authenticate"] == "Bearer"
