from functools import lru_cache
from secrets import token_urlsafe

from pwdlib import PasswordHash


class PasswordHasher:
    def __init__(self) -> None:
        self._password_hash = PasswordHash.recommended()

    def hash_password(self, plain_password: str) -> str:
        return self._password_hash.hash(plain_password)

    def verify_password(
        self,
        plain_password: str,
        password_hash: str,
    ) -> bool:
        return self._password_hash.verify(plain_password, password_hash)


@lru_cache(maxsize=1)
def get_dummy_password_hash() -> str:
    random_password = token_urlsafe(32)
    return PasswordHasher().hash_password(random_password)
