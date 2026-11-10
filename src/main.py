import argparse

import logging
import sys
from pathlib import Path

from pydantic import ValidationError

from conrad_parser.config import Settings
from conrad_parser.exceptions import ParserError
from conrad_parser.parsing import parse_card_html
from conrad_parser.scraper import run
from conrad_parser.validation import validate_row

log = logging.getLogger("conrad_parser")


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    ap = argparse.ArgumentParser(description="Scrape Balluff products from conrad.de to CSV")
    ap.add_argument("--limit", type=int, default=100, help="number of products to scrape")
    ap.add_argument("--out", type=Path, default=Path("balluff.csv"), help="CSV output path")
    ap.add_argument("--html", type=Path,
                    help="parse a saved product page HTML (no browser)")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--auth", action="store_true",
                   help="require login (fail otherwise)")
    g.add_argument("--guest", action="store_true",
                   help="ignore CONRAD_EMAIL/PASSWORD and run as Geschäftskunde")
    return ap.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    logging.basicConfig(level=logging.INFO, datefmt="%H:%M:%S",
                        format="%(asctime)s %(levelname)-7s %(message)s")

    if args.html:
        row = parse_card_html(args.html.read_text(encoding="utf-8"), str(args.html))
        row.validation_issues = validate_row(row)
        print(row.model_dump_json(by_alias=True, indent=1))
        return 0

    try:
        settings = Settings()
    except ValidationError as e:
        log.error("Invalid environment variables:\n%s", e)
        return 2

    mode = "auth" if args.auth else "guest" if args.guest else "auto"
    try:
        run(settings, args.limit, args.out, mode)
    except ParserError as e:
        log.error("%s", e)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
