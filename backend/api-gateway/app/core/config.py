from typing import List, Optional
from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        protected_namespaces=(),
    )

    # Downstream Microservices URLs
    auth_service_url: str = Field(
        default="http://localhost:8001",
        validation_alias=AliasChoices("AUTH_SERVICE_URL", "auth_service_url"),
    )
    food_service_url: str = Field(
        default="http://localhost:8002",
        validation_alias=AliasChoices("FOOD_SERVICE_URL", "food_service_url"),
    )
    food_service_ws_url: str = Field(
        default="ws://localhost:8002",
        validation_alias=AliasChoices("FOOD_SERVICE_WS_URL", "food_service_ws_url"),
    )
    agent_service_url: str = Field(
        default="http://localhost:8004",
        validation_alias=AliasChoices("AGENT_SERVICE_URL", "agent_service_url"),
    )

    # Google OAuth
    client_id: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("CLIENT_ID", "client_id"),
    )
    client_secret: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("CLIENT_SECRET", "client_secret"),
    )
    gateway_callback_url: str = Field(
        default="http://127.0.0.1:8000/api/auth/google/callback",
        validation_alias=AliasChoices("GATEWAY_CALLBACK_URL", "gateway_callback_url"),
    )

    # Session & Security
    session_secret_key: str = Field(
        default="gateway-session-secret-change-in-prod",
        validation_alias=AliasChoices("SESSION_SECRET_KEY", "session_secret_key"),
    )
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]
    request_timeout_seconds: float = 30.0


settings = Settings()
