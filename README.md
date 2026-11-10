# Parser

Scrapes Balluff product pages from [conrad.de](https://www.conrad.de/de/marken/balluff.html)
into a CSV file. The browser is real Google Chrome driven by
[patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright-python) with `headless=False`
and a persistent profile in `./profile`.

## How it works

**Login.** The scraper first checks whether the session stored in the browser profile is still
active: `api.conrad.de/session/1/userinfo` returns 200 only for a logged-in user. If it is not,
the scraper logs in the way a person would: it accepts the cookie banner, opens "Konto" →
"Anmelden", types the e-mail, clicks "Weiter", then types the password and clicks "Login". The
cursor moves along Bezier curves, text is typed with random pauses, and clicks land on a random
point inside each element. Cookies stay in the profile, so later runs skip the login. Without
credentials, or if the login fails, the scraper continues as a guest with "Geschäftskunde"
selected. The mode is recorded in the `session_mode` column.

**Data collection.** Product links are collected from the brand page (90 per page, further pages
via `?page=N`). Each product page is opened in the browser with scrolling and pauses, like a
user would. Data is taken from structured sources rather than the page markup: the Nuxt SSR
state `__NUXT_DATA__` (technical data, documents, description, EAN, part numbers, images),
JSON-LD (breadcrumbs), and the `/api/product/offers` XHR, which is intercepted when logged in
(all seller offers, stock, delivery and price tiers). In guest mode the offers are already part
of `__NUXT_DATA__`.

## Configuration

Credentials are optional:

```bash
cp env.example .env   # optionally fill in CONRAD_EMAIL / CONRAD_PASSWORD
```

The variables can also be set in the environment. They are validated with pydantic-settings:
either set both or neither.

## Running without Docker (Python only)

Requires Python 3.12+.

```bash
python3 -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt
patchright install chrome           # skip if Google Chrome is already installed

python src/main.py --limit 100 --out balluff.csv
```

A Chrome window opens, so you can watch the scraper work. On a Linux server without a screen,
use a virtual display: `sudo apt install xvfb`, then `xvfb-run -a python src/main.py`.

## Running in Docker

```bash
docker compose build
docker compose run --rm parser                                  # 100 products -> output/balluff.csv
docker compose run --rm parser --limit 10 --out output/test.csv --guest
```

Inside the container Chrome runs on an Xvfb virtual display. The browser profile (cookies,
session) is kept in the `chrome-profile` volume, results go to `./output`, debug snapshots to
`./debug`. Google Chrome for Linux is amd64-only, so on Apple Silicon the container runs under
emulation and is noticeably slower.

## Options

| Option | Description |
| --- | --- |
| `--limit N` | number of products to scrape (default 100) |
| `--out PATH` | CSV output path (default `balluff.csv`) |
| `--auth` | require login, fail otherwise |
| `--guest` | never log in, even if credentials are set |
| `--html PATH` | parse a saved product page HTML without a browser and print JSON |

## Output

Complex fields (`tech_data`, `documents`, `offers`, `price_tiers`) are stored in the CSV as JSON
strings. The row schema is defined in `src/conrad_parser/models/product.py`. Validation issues
(`no_offers`, `ean_checksum`, etc.) are written to the `validation_issues` column, and a summary
is printed at the end of the run. A page with critical issues is opened a second time.

## Project layout

```
src/
  main.py                 entry point (CLI)
  conrad_parser/
    config.py             settings (pydantic-settings), URLs and paths
    models/               pydantic schemas for the CSV row and offers
    parsing/              __NUXT_DATA__, JSON-LD and seller offer parsing
    browser/              Chrome launcher, human-like actions, Cloudflare
    ui/                   cookie banner, customer type dialog
    auth/                 session check and login
    scraper/              catalog and product page crawling, main loop
    validation/           row checks and the final report
    storage/              CSV writer
tests/                    parsing and validation tests (pytest)
```

Tests: `pip install pytest && pytest`.
