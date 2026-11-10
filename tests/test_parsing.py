import csv
import json

from conftest import CARD_URL, OFFERS, devalue_flatten

from conrad_parser.parsing import parse_card_html
from conrad_parser.parsing.nuxt import unflatten
from conrad_parser.storage import CSV_COLUMNS, to_csv_row, write_csv
from conrad_parser.validation import validate_row


def test_unflatten_roundtrip_and_wrappers():
    obj = {"a": [1, {"b": "x"}], "c": None}
    assert unflatten(devalue_flatten(obj)) == obj
    assert unflatten([{"v": 1}, ["Reactive", 2], 5]) == {"v": 5}


def test_guest_card(card_html):
    row = parse_card_html(card_html, CARD_URL)
    assert row.product_id == "2471385"
    assert row.title == "Balluff BES000H Induktiver Sensor"
    assert row.breadcrumbs == ["Startseite", "Sensorik", "Induktive Sensoren"]
    assert row.order_no == "2471385 - 62"
    assert row.produkt_art == "Induktiver Sensor"
    assert row.tech_data["Betriebsspannung max."] == "30 V/DC"
    assert row.datasheet_url.endswith("ds_de.pdf")
    assert row.offers_count == 2
    assert [o.fits_requested_qty for o in row.offers] == [True, False]
    assert row.total_price_net == 42.5 and row.stock == 7
    assert row.price_tiers[1].saved_percent == 6
    assert validate_row(row) == []


def test_offers_from_xhr_payload_take_precedence(card_html):
    payload = {"products": [{"productId": "002471385",
                             "offers": [OFFERS["ineligibleOffers"][0]]}]}
    row = parse_card_html(card_html, CARD_URL, payload)
    assert row.offers_count == 1 and row.shipped_by == "Other Seller"


def test_empty_page_is_flagged():
    row = parse_card_html("<html><h1>X</h1></html>", CARD_URL)
    issues = validate_row(row)
    assert {"no_offers", "bad_price", "no_tech_data"} <= set(issues)
    assert row.title == "X" and row.stock is None


def test_csv_row(card_html, tmp_path):
    row = parse_card_html(card_html, CARD_URL)
    row.session_mode = "guest"
    out = to_csv_row(row)
    assert list(out) == CSV_COLUMNS
    assert out["Produkt-Art"] == "Induktiver Sensor"
    assert out["breadcrumbs"] == "Startseite > Sensorik > Induktive Sensoren"
    assert json.loads(out["offers"])[0]["seller"] == "Conrad Electronic"
    assert out["validation_issues"] == ""

    path = tmp_path / "out" / "rows.csv"
    write_csv([row], path)
    with path.open(encoding="utf-8-sig") as f:
        assert next(csv.DictReader(f))["product_id"] == "2471385"
