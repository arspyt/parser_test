"""Human-like actions: Bezier-curve mouse movement, clicks, scrolling, typing."""
import random
import time

from patchright.sync_api import Error as PlaywrightError
from patchright.sync_api import Locator, Page


def pause(a: float = 0.8, b: float = 2.2) -> None:
    time.sleep(random.uniform(a, b))


class Human:
    """Actions on a single tab. Remembers the cursor position between moves."""

    def __init__(self, page: Page):
        self.page = page
        self._x: float | None = None
        self._y: float | None = None

    def viewport(self) -> tuple[int, int]:
        try:
            w, h = self.page.evaluate("[window.innerWidth, window.innerHeight]")
            return int(w), int(h)
        except (PlaywrightError, TypeError, ValueError):
            return 1280, 800

    def move(self, x: float, y: float) -> None:
        """Smooth cursor movement along a Bezier curve with slight jitter and varying speed."""
        w, h = self.viewport()
        sx = self._x if self._x is not None else random.uniform(0.2, 0.8) * w
        sy = self._y if self._y is not None else random.uniform(0.2, 0.8) * h
        c1 = (sx + (x - sx) * random.uniform(0.2, 0.4) + random.uniform(-80, 80),
              sy + (y - sy) * random.uniform(0.0, 0.3) + random.uniform(-80, 80))
        c2 = (sx + (x - sx) * random.uniform(0.6, 0.9) + random.uniform(-60, 60),
              sy + (y - sy) * random.uniform(0.7, 1.0) + random.uniform(-60, 60))
        dist = ((x - sx) ** 2 + (y - sy) ** 2) ** 0.5
        steps = max(12, min(60, int(dist / 12)))
        for i in range(1, steps + 1):
            t = i / steps
            t = t * t * (3 - 2 * t)                      # ease-in-out
            bx = ((1 - t) ** 3 * sx + 3 * (1 - t) ** 2 * t * c1[0]
                  + 3 * (1 - t) * t ** 2 * c2[0] + t ** 3 * x)
            by = ((1 - t) ** 3 * sy + 3 * (1 - t) ** 2 * t * c1[1]
                  + 3 * (1 - t) * t ** 2 * c2[1] + t ** 3 * y)
            self.page.mouse.move(bx + random.uniform(-0.8, 0.8), by + random.uniform(-0.8, 0.8))
            time.sleep(random.uniform(0.004, 0.016))
        self.page.mouse.move(x, y)
        self._x, self._y = x, y

    def click(self, locator: Locator) -> None:
        """Move to the element, hesitate briefly and click a random point inside it."""
        locator.scroll_into_view_if_needed(timeout=8000)
        pause(0.2, 0.6)
        box = locator.bounding_box()
        if not box:
            locator.click()
            return
        x = box["x"] + box["width"] * random.uniform(0.25, 0.75)
        y = box["y"] + box["height"] * random.uniform(0.3, 0.7)
        self.move(x, y)
        time.sleep(random.uniform(0.12, 0.45))
        self.page.mouse.down()
        time.sleep(random.uniform(0.04, 0.14))
        self.page.mouse.up()

    def scroll(self, total: int = 2500) -> None:
        """Scroll in uneven steps, sometimes scrolling back up a little."""
        done = 0
        while done < total:
            step = random.randint(150, 420)
            self.page.mouse.wheel(0, step)
            done += step
            time.sleep(random.uniform(0.15, 0.7))
            if random.random() < 0.12:
                self.page.mouse.wheel(0, -random.randint(60, 200))
                time.sleep(random.uniform(0.2, 0.5))

    def wander(self, n: int | None = None) -> None:
        """A few random cursor movements across the page."""
        w, h = self.viewport()
        for _ in range(n or random.randint(2, 4)):
            self.move(random.uniform(0.1, 0.9) * w, random.uniform(0.15, 0.85) * h)
            time.sleep(random.uniform(0.1, 0.6))

    def type(self, locator: Locator, text: str) -> None:
        self.click(locator)
        time.sleep(random.uniform(0.2, 0.5))
        for ch in text:
            self.page.keyboard.type(ch)
            time.sleep(random.uniform(0.05, 0.19))
            if random.random() < 0.06:
                time.sleep(random.uniform(0.2, 0.5))
