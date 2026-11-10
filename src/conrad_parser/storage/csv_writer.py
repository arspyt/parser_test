"""CSV output: lists are joined with a separator, complex fields are stored as JSON strings."""
import csv
import json
from pathlib import Path

from conrad_parser.models import ProductRow

CSV_COLUMNS = [f.alias or name for name, f in ProductRow.model_fields.items()]
_JOINERS = {"breadcrumbs": " > ", "image_urls": " | ", "validation_issues": "; "}


def to_csv_row(row: ProductRow) -> dict[str, str | int | float | bool]:
    out = {}
    for key, value in row.model_dump(mode="json", by_alias=True).items():
        if key in _JOINERS:
            value = _JOINERS[key].join(value)
        elif isinstance(value, (dict, list)):
            value = json.dumps(value, ensure_ascii=False)
        elif value is None:
            value = ""
        out[key] = value
    return out


def write_csv(rows: list[ProductRow], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        w.writeheader()
        w.writerows(to_csv_row(r) for r in rows)
