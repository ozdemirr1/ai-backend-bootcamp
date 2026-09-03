from datetime import timedelta

import jwt
from jwt.exceptions import InvalidTokenError

from ticket_api.clock import Clock

ACCESS_TOKEN_ALGORITHM = "HS256"


class InvalidAccessTokenError(Exception):
    pass


class JwtAccessTokenManager:
    def __init__(
        self,
        *,
        secret: str,
        lifetime: timedelta,
        clock: Clock,
    ) -> None:
        if not isinstance(secret, str) or not secret:
            raise ValueError("secret cannot be empty")

        if lifetime <= timedelta(0):
            raise ValueError("lifetime must be positive")

        self._secret = secret
        self._lifetime = lifetime
        self._clock = clock

    def create_access_token(self, user_id: int) -> str:
        if type(user_id) is not int:
            raise TypeError("user_id must be an int")
        if user_id <= 0:
            raise ValueError("user_id must be positive")

        issued_at = self._clock.now()

        if issued_at.tzinfo is None or issued_at.utcoffset() is None:
            raise ValueError("clock must return a timezone-aware datetime")

        payload = {
            "sub": str(user_id),
            "iat": issued_at,
            "exp": issued_at + self._lifetime,
        }

        return jwt.encode(
            payload,
            self._secret,
            algorithm=ACCESS_TOKEN_ALGORITHM,
        )

    def decode_access_token(self, token: str) -> int:
        if not isinstance(token, str) or not token:
            raise InvalidAccessTokenError("Invalid access token")

        try:
            payload = jwt.decode(
                token,
                self._secret,
                algorithms=[ACCESS_TOKEN_ALGORITHM],
                options={
                    "require": ["sub", "iat", "exp"],
                },
            )
        except InvalidTokenError as exc:
            raise InvalidAccessTokenError("Invalid access token") from exc

        subject = payload["sub"]

        if not isinstance(subject, str):
            raise InvalidAccessTokenError("Invalid access token")

        try:
            user_id = int(subject)
        except ValueError as exc:
            raise InvalidAccessTokenError("Invalid access token") from exc

        if user_id <= 0:
            raise InvalidAccessTokenError("Invalid access token")

        return user_id
