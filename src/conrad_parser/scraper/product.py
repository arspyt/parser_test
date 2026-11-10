import logging
import random
import time

from patchright.sync_api import Error as PlaywrightError
from patchright.sync_api import Page, Response

from conrad_parser.browser import Human, pause, wait_cloudflare
from conrad_parser.config import BRAND_URL
from conrad_parser.models import ProductRow
from conrad_parser.parsing import parse_card_html
from conrad_parser.validation import CRITICAL, validate_row

log = logging.getLogger(__name__)


class OffersCapture:
    """Captures the POST /api/product/offers XHR that the page uses to load offers."""

    def __init__(self, page: Page):
        self.payload: dict | None = None
        page.on("response", self._on_response)

    def _on_response(self, resp: Response) -> None:
        if "/api/product/offers" not in resp.url or resp.request.method != "POST":
            return
        try:
            self.payload = resp.json()
        except (PlaywrightError, ValueError) as e:
            log.debug("Could not read /api/product/offers response: %s", e)


def fetch_card(human: Human, url: str, cap: OffersCapture) -> tuple[str, dict | None]:
    """Open the product page like a user; return the HTML and the offers XHR response."""
    page = human.page
    cap.payload = None
    page.goto(url, referer=BRAND_URL)
    wait_cloudflare(page)
    page.wait_for_selector("script#__NUXT_DATA__", state="attached", timeout=30_000)
    page.wait_for_selector("h1", timeout=30_000)
    pause(0.8, 1.5)
    human.wander()
    human.scroll(random.randint(1200, 3000))
    page.mouse.wheel(0, -random.randint(300, 900))
    for _ in range(20):                 # wait for the offers XHR (up to ~10 s)
        if cap.payload:
            break
        time.sleep(0.5)
    pause(0.4, 1.0)
    return page.content(), cap.payload


def scrape_product(human: Human, url: str, cap: OffersCapture) -> ProductRow:
    """Scrape and validate a product. On critical issues (the page may not have
    finished loading) open it once more and keep the better result."""
    html, payload = fetch_card(human, url, cap)
    row = parse_card_html(html, url, payload)
    issues = validate_row(row)
    if critical := CRITICAL & set(issues):
        log.info("Critical issues %s, retrying: %s", sorted(critical), url)
        pause(2, 4)
        html, payload = fetch_card(human, url, cap)
        row2 = parse_card_html(html, url, payload)
        issues2 = validate_row(row2)
        if len(issues2) <= len(issues):
            row, issues = row2, issues2
    row.validation_issues = issues
    return row
