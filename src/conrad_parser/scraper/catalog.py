import logging
import random
import re

from patchright.sync_api import Error as PlaywrightError

from conrad_parser.browser import Human, dump_debug, pause, wait_cloudflare
from conrad_parser.config import BASE_URL, BRAND_URL

log = logging.getLogger(__name__)


def collect_links(human: Human, limit: int) -> list[str]:
    """The brand page lists 90 products; further pages are ?page=N."""
    page = human.page
    links: list[str] = []
    n = 1
    while len(links) < limit:
        url = BRAND_URL if n == 1 else f"{BRAND_URL}?page={n}"
        page.goto(url, referer=BASE_URL + "/")
        wait_cloudflare(page)
        try:
            page.wait_for_selector("a[href*='/de/p/']", timeout=30_000)
        except PlaywrightError:
            log.warning("No product links on listing page %d", n)
            dump_debug(page, f"list_{n}")
            break
        human.wander(2)
        human.scroll(random.randint(3500, 6000))   # also triggers lazy loading
        hrefs = re.findall(r'href="(/de/p/[^"#?]+\.html)"', page.content())
        new = [BASE_URL + h for h in dict.fromkeys(hrefs) if BASE_URL + h not in links]
        log.info("Listing page %d: +%d (total %d)", n, len(new), len(links) + len(new))
        if not new:
            break
        links.extend(new)
        n += 1
        pause(1.5, 3)
    return links[:limit]
