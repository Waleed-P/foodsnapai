from typing import List
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Database
    database_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/foodsnap_db",
        validation_alias=AliasChoices("DATABASE_URL", "database_url"),
    )

    # JWT Authentication
    jwt_secret_key: str = Field(
        default="foodsnapaijwttokensecretkey",
        validation_alias=AliasChoices("JWT_SECRET_KEY", "JWT_SECRET", "jwt_secret_key"),
    )
    jwt_algorithm: str = Field(
        default="HS256",
        validation_alias=AliasChoices("JWT_ALGORITHM", "jwt_algorithm"),
    )
    access_token_expire_days: int = 1
    refresh_token_expire_days: int = 7

    # OAuth Google
    client_id: str | None = Field(
        default=None,
        validation_alias=AliasChoices("CLIENT_ID", "client_id"),
    )
    client_secret: str | None = Field(
        default=None,
        validation_alias=AliasChoices("CLIENT_SECRET", "client_secret"),
    )

    # Session & Cookies
    session_secret_key: str = Field(
        default="foodsnap-session-secret-change-in-prod",
        validation_alias=AliasChoices("SESSION_SECRET_KEY", "session_secret_key"),
    )
    cookie_secure: bool = Field(
        default=False,
        validation_alias=AliasChoices("COOKIE_SECURE", "cookie_secure"),
    )
    cookie_samesite: str = Field(
        default="lax",
        validation_alias=AliasChoices("COOKIE_SAMESITE", "cookie_samesite"),
    )

    # URLs
    frontend_url: str = Field(
        default="http://localhost:3000",
        validation_alias=AliasChoices("FRONTEND_URL", "frontend_url"),
    )
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://api-gateway:8000",
    ]


settings = Settings()
