import logging
import re

from patchright.sync_api import Error as PlaywrightError

from conrad_parser.browser import Human, pause

log = logging.getLogger(__name__)

_ACCEPT_NAMES = re.compile(
    r"^(Annehmen|Alle akzeptieren|Alle Cookies akzeptieren|Akzeptieren)$", re.IGNORECASE)


def accept_cookies(human: Human, wait_ms: int = 6000) -> bool:
    """The Usercentrics banner ("Anpassen" / "Annehmen" buttons) lives in the
    #usercentrics-root shadow DOM; Playwright locators pierce it."""
    page = human.page
    candidates = [
        page.get_by_role("button", name=_ACCEPT_NAMES).first,
        page.locator("#usercentrics-root button:has-text('Annehmen')").first,
        page.locator("[data-testid='uc-accept-all-button']").first,
    ]
    for btn in candidates:
        try:
            btn.wait_for(state="visible", timeout=wait_ms)
            human.click(btn)
            pause(1, 2)
            log.info("Cookie banner accepted")
            return True
        except PlaywrightError:
            wait_ms = 1500          # no banner or already closed: try the rest quickly
    return False
