"""Lightweight checks of a scraped row. Issues go to the validation_issues column."""
import re
from itertools import pairwise

from conrad_parser.models import KEY_SPECS, ProductRow

# these issues usually mean the page did not finish loading, so it is worth reopening
CRITICAL = frozenset({"no_title", "no_tech_data", "no_offers", "bad_price"})


def ean13_ok(code: str) -> bool:
    if not re.fullmatch(r"\d{13}", code or ""):
        return False
    d = [int(c) for c in code]
    return (10 - (sum(d[:12:2]) + 3 * sum(d[1:12:2])) % 10) % 10 == d[12]


def validate_row(row: ProductRow) -> list[str]:
    """Returns a list of issue codes (empty means the row is fine)."""
    issues = []

    pid = row.product_id
    if not re.fullmatch(r"\d+", pid) or not row.url.endswith(f"-{pid}.html"):
        issues.append("product_id_mismatch")
    if not row.title:
        issues.append("no_title")
    if len([c for c in row.breadcrumbs if c]) < 2:
        issues.append("no_breadcrumbs")
    if not re.fullmatch(r"\d{13}", row.ean):
        issues.append("bad_ean_format")
    elif not ean13_ok(row.ean):
        issues.append("ean_checksum")
    if not row.manufacturer_part_no:
        issues.append("no_manufacturer_part_no")
    if not re.fullmatch(r"\d+(\s*-\s*\d+)?", row.order_no):
        issues.append("bad_order_no")
    imgs = [u for u in row.image_urls if u]
    if not imgs or not all(u.startswith("https://") for u in imgs):
        issues.append("bad_images")
    if not row.datasheet_url:
        issues.append("no_datasheet")
    elif not row.datasheet_url.startswith("https://"):
        issues.append("bad_datasheet_url")

    if not row.tech_data:
        issues.append("no_tech_data")
    else:
        issues.extend(f"no_spec:{k}" for k in KEY_SPECS if not row.tech_data.get(k))

    if not row.offers:
        issues.append("no_offers")
    if any(not o.seller or o.unit_price_net is None or o.unit_price_net <= 0
           for o in row.offers):
        issues.append("bad_offer")
    if row.total_price_net is None or row.total_price_net <= 0:
        issues.append("bad_price")
    if row.shipping is not None and row.shipping < 0:
        issues.append("bad_shipping")
    if row.stock is not None and row.stock < 0:
        issues.append("bad_stock")
    ppu = [t.price_per_unit for t in row.price_tiers]
    if any(x is None for x in ppu) or any(b > a for a, b in pairwise(ppu)):
        issues.append("bad_price_tiers")
    return issues
