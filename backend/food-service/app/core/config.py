from pathlib import Path
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

    # Database
    database_url: str = Field(
        default="postgresql://postgres:postgres@localhost:5432/foodsnap_db",
        validation_alias=AliasChoices("DATABASE_URL", "database_url"),
    )

    # Redis
    redis_url: str = Field(
        default="redis://localhost:6379/0",
        validation_alias=AliasChoices("REDIS_URL", "redis_url"),
    )
    redis_host: str = Field(
        default="localhost",
        validation_alias=AliasChoices("REDIS_HOST", "redis_host"),
    )
    redis_port: int = Field(
        default=6379,
        validation_alias=AliasChoices("REDIS_PORT", "redis_port"),
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

    # AWS S3 Storage
    aws_region: str = Field(
        default="ap-southeast-2",
        validation_alias=AliasChoices("AWS_REGION", "AWS_DEFAULT_REGION", "aws_region"),
    )
    aws_bucket_name: str = Field(
        default="foodsnapai-image-bucket",
        validation_alias=AliasChoices("AWS_STORAGE_BUCKET_NAME", "AWS_S3_BUCKET", "aws_bucket_name"),
    )
    aws_access_key_id: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("AWS_ACCESS_KEY_ID", "aws_access_key_id"),
    )
    aws_secret_access_key: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("AWS_SECRET_ACCESS_KEY", "aws_secret_access_key"),
    )

    # Spoonacular / USDA Nutrition API
    spoonacular_api_key: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("SPOONACULAR_API_KEY", "spoonacular_api_key"),
    )
    spoonacular_url: str = Field(
        default="https://api.spoonacular.com/food/products/search",
        validation_alias=AliasChoices("SPOONACULAR_URL", "spoonacular_url"),
    )

    # Machine Learning Model
    model_path: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("MODEL_PATH", "model_path"),
    )

    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://api-gateway:8000",
    ]

    def get_effective_model_path(self) -> Path:
        """Resolve model path cleanly with fallback to bundled utilities model."""
        if self.model_path and Path(self.model_path).exists():
            return Path(self.model_path)
        
        fallback = Path(__file__).resolve().parent.parent / "utilities" / "foodsnap_efficientnet_final.keras"
        return fallback

    def get_effective_class_names_path(self) -> Path:
        return Path(__file__).resolve().parent.parent / "utilities" / "class_names.json"


settings = Settings()
