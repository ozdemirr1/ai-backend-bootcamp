from functools import lru_cache
from typing import Annotated

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

JwtSecret = Annotated[
    SecretStr,
    Field(min_length=32),
]

AccessTokenExpireMinutes = Annotated[
    int,
    Field(ge=1, le=1440),
]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        frozen=True,
    )

    database_url: SecretStr
    jwt_secret: JwtSecret
    access_token_expire_minutes: AccessTokenExpireMinutes = 30


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
