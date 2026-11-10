import pytest
from conftest import CARD_URL
from pydantic import ValidationError

from conrad_parser.config import Settings
from conrad_parser.models import PriceScale
from conrad_parser.parsing import parse_card_html
from conrad_parser.validation import ean13_ok, validate_row


def test_ean13():
    assert ean13_ok("4030664105465")
    assert not ean13_ok("4030664105468")
    assert not ean13_ok("12345")


def test_rising_price_tiers_flagged(card_html):
    row = parse_card_html(card_html, CARD_URL)
    row.price_tiers = [PriceScale(qty=1, price_per_unit=1.0), PriceScale(qty=10, price_per_unit=2.0)]
    assert "bad_price_tiers" in validate_row(row)


def test_settings_optional(monkeypatch):
    monkeypatch.delenv("CONRAD_EMAIL", raising=False)
    monkeypatch.delenv("CONRAD_PASSWORD", raising=False)
    assert not Settings(_env_file=None).has_credentials


def test_settings_credentials(monkeypatch):
    monkeypatch.setenv("CONRAD_EMAIL", "a@b.de")
    monkeypatch.setenv("CONRAD_PASSWORD", "secret")
    s = Settings(_env_file=None)
    assert s.has_credentials and s.conrad_password.get_secret_value() == "secret"
    assert "secret" not in repr(s)


def test_settings_require_both(monkeypatch):
    monkeypatch.setenv("CONRAD_EMAIL", "a@b.de")
    monkeypatch.delenv("CONRAD_PASSWORD", raising=False)
    with pytest.raises(ValidationError):
        Settings(_env_file=None)
