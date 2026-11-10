import logging
from typing import Literal

from conrad_parser.auth.login import is_logged_in, login
from conrad_parser.browser import Human, wait_cloudflare
from conrad_parser.config import BASE_URL, Settings
from conrad_parser.exceptions import AuthError
from conrad_parser.models import SessionMode
from conrad_parser.ui import accept_cookies, choose_business_customer

log = logging.getLogger(__name__)

RunMode = Literal["auto", "auth", "guest"]


def establish_session(human: Human, settings: Settings, mode: RunMode) -> SessionMode:
    """Open the home page and prepare the browser: log in if credentials are set,
    otherwise use guest mode as Geschäftskunde."""
    page = human.page
    want_auth = mode != "guest" and settings.has_credentials
    page.goto(BASE_URL + "/")
    wait_cloudflare(page)
    accept_cookies(human)

    session: SessionMode = "guest"
    if want_auth:
        if is_logged_in(page):
            log.info("Session from the profile is active, no login needed")
            session = "auth"
        elif login(human, settings.conrad_email, settings.conrad_password.get_secret_value()):
            session = "auth"
        elif mode == "auth":
            raise AuthError("Could not log in (see debug/login_failed.*)")
        else:
            log.warning("Continuing without login (Geschäftskunde)")
            page.goto(BASE_URL + "/")
            wait_cloudflare(page)
    else:
        log.info("No credentials set: running without login")
    if session == "guest":
        choose_business_customer(human)
    return session
