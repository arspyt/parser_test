from pathlib import Path

from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROFILE_DIR = PROJECT_ROOT / "profile"
DEBUG_DIR = PROJECT_ROOT / "debug"

BASE_URL = "https://www.conrad.de"
BRAND_URL = f"{BASE_URL}/de/marken/balluff.html"
USERINFO_URL = ("https://api.conrad.de/session/1/userinfo"
                "?apikey=5fFNAUWeVNK6A3pvamgJdw8jymZVeKrM3ak2J7GCGvYbFgGm")


class Settings(BaseSettings):
    """Environment variables (or a .env file in the project root). Both are optional:
    without them the scraper runs in guest mode as Geschäftskunde."""

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        str_strip_whitespace=True,
        extra="ignore",
    )

    conrad_email: str | None = None
    conrad_password: SecretStr | None = None

    @model_validator(mode="after")
    def _both_or_none(self) -> "Settings":
        if bool(self.conrad_email) != bool(self.conrad_password):
            raise ValueError("CONRAD_EMAIL and CONRAD_PASSWORD must be set together (or not at all)")
        return self

    @property
    def has_credentials(self) -> bool:
        return bool(self.conrad_email and self.conrad_password)
