"""Customer type dialog (Privatkunde / Geschäftskunde)."""
import logging

from patchright.sync_api import Error as PlaywrightError
from patchright.sync_api import Locator

from conrad_parser.browser import Human, dump_debug, pause

log = logging.getLogger(__name__)


def _business_button(human: Human) -> Locator:
    # not by text: the header label also says "Geschäftskunde" and is hidden in narrow windows
    return human.page.locator("button[aria-label='Als Geschäftskunde weiterfahren']").first


def choose_business_customer(human: Human) -> None:
    btn = _business_button(human)
    try:
        btn.wait_for(state="visible", timeout=10_000)
        human.wander(2)
        human.click(btn)
        pause(1.5, 3)
        log.info("Geschäftskunde selected")
    except PlaywrightError:
        log.warning("Geschäftskunde dialog did not appear (probably already selected)")
        dump_debug(human.page, "no_geschaeftskunde")


def dismiss_customer_dialog(human: Human) -> None:
    """If the dialog is shown, pick Geschäftskunde (after login the role is
    determined by the account anyway)."""
    btn = _business_button(human)
    try:
        btn.wait_for(state="visible", timeout=2500)
    except PlaywrightError:
        return
    try:
        human.click(btn)
        pause(1.5, 2.5)
    except PlaywrightError as e:
        log.debug("Customer type dialog not handled: %s", e)
