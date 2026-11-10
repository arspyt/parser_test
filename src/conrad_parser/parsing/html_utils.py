import html as htmllib
import json
import re


def html_to_text(html: str) -> str:
    t = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    t = re.sub(r"<script.*?</script>|<style.*?</style>", "", t, flags=re.DOTALL)
    t = htmllib.unescape(re.sub(r"<[^>]+>", " ", t))
    return re.sub(r"\s+", " ", t)


def first(rx: str, text: str, flags: int = 0) -> str:
    m = re.search(rx, text, flags)
    return m.group(1).strip() if m else ""


def jsonld(html: str, hid: str) -> dict | None:
    m = re.search(rf'<script[^>]*data-hid="{re.escape(hid)}"[^>]*>(.*?)</script>', html,
                  re.DOTALL)
    try:
        return json.loads(m.group(1)) if m else None
    except ValueError:
        return None
