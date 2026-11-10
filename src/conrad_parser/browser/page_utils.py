import logging

from patchright.sync_api import Error as PlaywrightError
from patchright.sync_api import Page

from conrad_parser.config import DEBUG_DIR

log = logging.getLogger(__name__)

_CF_PASSED_JS = "!/just a moment|einen moment|verifying/i.test(document.title)"


def dump_debug(page: Page, name: str) -> None:
    """Save the current page HTML and a screenshot to debug/ for troubleshooting."""
    try:
        DEBUG_DIR.mkdir(parents=True, exist_ok=True)
        (DEBUG_DIR / f"{name}.html").write_text(page.content(), encoding="utf-8")
        page.screenshot(path=str(DEBUG_DIR / f"{name}.png"))
    except (PlaywrightError, OSError) as e:
        log.warning("Could not save debug/%s: %s", name, e)


def wait_cloudflare(page: Page, timeout: int = 90_000) -> None:
    try:
        page.wait_for_function(_CF_PASSED_JS, timeout=timeout)
    except PlaywrightError:
        log.warning("Cloudflare: complete the check manually in the browser window")
        dump_debug(page, "cloudflare")
        page.wait_for_function(_CF_PASSED_JS, timeout=180_000)
