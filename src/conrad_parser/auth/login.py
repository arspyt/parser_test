import logging
import re

from patchright.sync_api import Error as PlaywrightError
from patchright.sync_api import Page

from conrad_parser.browser import Human, dump_debug, pause, wait_cloudflare
from conrad_parser.config import USERINFO_URL
from conrad_parser.ui import accept_cookies, dismiss_customer_dialog

log = logging.getLogger(__name__)


def is_logged_in(page: Page) -> bool:
    """userinfo returns 200 only for an active session (401 for guests)."""
    try:
        status = page.evaluate(
            "(u) => fetch(u, {credentials: 'include'}).then(r => r.status)", USERINFO_URL)
        return status == 200
    except PlaywrightError:
        return False


def _open_login_form(human: Human) -> None:
    page = human.page
    konto = page.locator("button[aria-label='Konto']").first
    # text-is: exact case-sensitive match, otherwise "Jetzt anmelden" from the
    # newsletter block in the footer would match too
    anmelden = page.locator("button:text-is('Anmelden'):visible, "
                            "a:text-is('Anmelden'):visible").first
    for attempt in range(3):            # the panel may not open on the first click
        human.click(konto)
        try:
            anmelden.wait_for(state="visible", timeout=5000)
            break
        except PlaywrightError:
            log.info("'Konto' panel did not open, retry %d/3", attempt + 1)
            dismiss_customer_dialog(human)
            pause(1, 2)
    else:
        raise RuntimeError("'Anmelden' button did not appear")
    pause(0.6, 1.2)
    human.click(anmelden)


def login(human: Human, email: str, password: str) -> bool:
    """Konto -> Anmelden -> e-mail -> Weiter -> password -> Login. Returns True on success."""
    page = human.page
    try:
        accept_cookies(human, 3000)
        dismiss_customer_dialog(human)      # the customer type dialog covers the header
        human.wander(2)
        _open_login_form(human)
        page.wait_for_url(re.compile(r"accounts\.conrad\.com"), timeout=30_000)
        wait_cloudflare(page)
        accept_cookies(human)

        pause(1, 2)
        human.type(page.locator("input[name='username']").first, email)
        pause(0.5, 1.2)
        human.click(page.locator("button[aria-label='Weiter']").first)

        pw = page.locator("input[name='password']").first
        pw.wait_for(state="visible", timeout=30_000)
        pause(0.8, 1.6)
        human.type(pw, password)
        pause(0.5, 1.2)
        human.click(page.locator("button[aria-label='Login']").first)

        page.wait_for_url(re.compile(r"https://www\.conrad\.de/"), timeout=60_000)
        page.wait_for_load_state("domcontentloaded")
        pause(2, 3)
        ok = is_logged_in(page)
        if ok:
            log.info("Logged in")
        else:
            log.warning("Session not confirmed after login")
        return ok
    except (PlaywrightError, RuntimeError) as e:
        log.warning("Login failed: %s: %s", type(e).__name__, str(e)[:150])
        dump_debug(page, "login_failed")
        return False
