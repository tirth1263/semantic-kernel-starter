"""Environment-backed configuration for the starter agent."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


DEFAULT_BASE_URL = "https://api.tokenfactory.nebius.com/v1/"
DEFAULT_MODEL = "Qwen/Qwen3-30B-A3B"
DEFAULT_SERVICE_ID = "nebius"
DEFAULT_TIMEZONE = "America/Phoenix"


@dataclass(frozen=True)
class AppSettings:
    """Runtime settings used to configure Semantic Kernel and Nebius."""

    nebius_api_key: str
    nebius_base_url: str = DEFAULT_BASE_URL
    nebius_model: str = DEFAULT_MODEL
    service_id: str = DEFAULT_SERVICE_ID
    default_timezone: str = DEFAULT_TIMEZONE
    temperature: float = 0.6
    max_tokens: int | None = 1000

    @classmethod
    def from_env(cls) -> "AppSettings":
        """Load settings from environment variables and a local .env file."""

        load_dotenv()

        api_key = _required_env("NEBIUS_API_KEY")
        base_url = os.getenv("NEBIUS_BASE_URL", DEFAULT_BASE_URL).strip()

        return cls(
            nebius_api_key=api_key,
            nebius_base_url=_normalize_base_url(base_url),
            nebius_model=os.getenv("NEBIUS_MODEL", DEFAULT_MODEL).strip() or DEFAULT_MODEL,
            service_id=os.getenv("SERVICE_ID", DEFAULT_SERVICE_ID).strip() or DEFAULT_SERVICE_ID,
            default_timezone=os.getenv("DEFAULT_TIMEZONE", DEFAULT_TIMEZONE).strip() or DEFAULT_TIMEZONE,
            temperature=_env_float("TEMPERATURE", 0.6),
            max_tokens=_env_optional_int("MAX_TOKENS", 1000),
        )


def _required_env(name: str) -> str:
    value = os.getenv(name, "").strip()
    if not value or value == "your_nebius_api_key_here":
        raise RuntimeError(
            f"{name} is missing. Copy .env.example to .env and set your Nebius API key."
        )
    return value


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name, "").strip()
    if not value:
        return default
    try:
        return float(value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be a number, got {value!r}.") from exc


def _env_optional_int(name: str, default: int | None) -> int | None:
    value = os.getenv(name, "").strip()
    if not value:
        return default
    if value.lower() in {"none", "null", "false", "off"}:
        return None
    try:
        parsed = int(value)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer, got {value!r}.") from exc
    return parsed if parsed > 0 else None


def _normalize_base_url(base_url: str) -> str:
    if not base_url:
        return DEFAULT_BASE_URL
    return base_url.rstrip("/") + "/"

