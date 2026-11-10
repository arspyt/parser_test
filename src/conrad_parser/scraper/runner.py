import logging
from pathlib import Path

from conrad_parser.auth import RunMode, establish_session
from conrad_parser.browser import Human, dump_debug, open_browser, pause
from conrad_parser.config import Settings
from conrad_parser.exceptions import AuthError
from conrad_parser.models import ProductRow
from conrad_parser.scraper.catalog import collect_links
from conrad_parser.scraper.product import OffersCapture, scrape_product
from conrad_parser.storage import write_csv
from conrad_parser.validation import log_report

log = logging.getLogger(__name__)


def run(settings: Settings, limit: int, out: Path, mode: RunMode = "auto") -> list[ProductRow]:
    if mode == "auth" and not settings.has_credentials:
        raise AuthError("--auth mode: set CONRAD_EMAIL and CONRAD_PASSWORD (env or .env)")

    rows: list[ProductRow] = []
    with open_browser() as page:
        human = Human(page)
        session = establish_session(human, settings, mode)
        cap = OffersCapture(page)
        links = collect_links(human, limit)
        log.info("Product links: %d (mode: %s)", len(links), session)

        for i, url in enumerate(links, 1):
            try:
                row = scrape_product(human, url, cap)
                row.session_mode = session
                rows.append(row)
                flag = f" | issues: {len(row.validation_issues)}" if row.validation_issues else ""
                log.info("[%d/%d] %s %s | offers: %d%s", i, len(links),
                         row.product_id, row.title[:55], row.offers_count, flag)
            except Exception as e:  # noqa: BLE001 - one broken page must not stop the run
                log.error("[%d/%d] ERROR %s: %s", i, len(links), url, e)
                dump_debug(page, f"error_{i}")
            pause(1.5, 3.5)

    if rows:
        write_csv(rows, out)
        log.info("Saved %d rows to %s", len(rows), out)
        log_report(rows)
    return rows
