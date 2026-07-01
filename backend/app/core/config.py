"""Application configuration.

Implements handbook Chapter 15 (API Architecture) environment-driven
configuration and ADR-010's requirement that switching AI providers
(rule-based vs. OpenAI-compatible, hosted or on-premises) is a
configuration change, never a code change.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_prefix="FARMOS_", extra="ignore")

    app_name: str = "Origami FarmOS API"
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql+psycopg://postgres:postgres@localhost:5432/farmos"

    # JWT (Chapter 17 - Security)
    secret_key: str = "dev-secret-change-me"
    access_token_expire_minutes: int = 60 * 12

    # AI provider selection (ADR-010). "rule_based" is the only provider
    # enabled by default; "openai_compatible" works against either the
    # hosted OpenAI API or a future on-premises OpenAI-compatible endpoint,
    # selected purely by base_url/api_key, never by code changes.
    ai_provider: str = "rule_based"
    openai_base_url: str = "https://api.openai.com/v1"
    openai_api_key: str | None = None
    openai_model: str = "gpt-4o-mini"

    # Inventory/feed forecast threshold (Chapter 6 REQ-FEED-102, Chapter 10 REQ-INV-102)
    inventory_low_stock_days_threshold: int = 7


@lru_cache
def get_settings() -> Settings:
    return Settings()
