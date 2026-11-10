from collections.abc import Iterator
from contextlib import contextmanager

from patchright.sync_api import Page, sync_playwright

from conrad_parser.config import PROFILE_DIR


@contextmanager
def open_browser() -> Iterator[Page]:
    """Real Chrome with a persistent profile: cookies and the session survive restarts.
    headless=False is required (without a screen, use the Xvfb virtual display)."""
    with sync_playwright() as p:
        ctx = p.chromium.launch_persistent_context(
            user_data_dir=str(PROFILE_DIR), channel="chrome",
            headless=False, no_viewport=True)
        try:
            yield ctx.pages[0] if ctx.pages else ctx.new_page()
        finally:
            ctx.close()
