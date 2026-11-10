# Graph Report - conrad_parser  (2026-11-10)

## Corpus Check
- 36 files · ~5,918 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 902 nodes · 1790 edges · 90 communities (84 shown, 6 thin omitted)
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 180 edges (avg confidence: 0.75)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]
- [[_COMMUNITY_Community 18|Community 18]]
- [[_COMMUNITY_Community 19|Community 19]]
- [[_COMMUNITY_Community 20|Community 20]]
- [[_COMMUNITY_Community 21|Community 21]]
- [[_COMMUNITY_Community 22|Community 22]]
- [[_COMMUNITY_Community 23|Community 23]]
- [[_COMMUNITY_Community 24|Community 24]]
- [[_COMMUNITY_Community 25|Community 25]]
- [[_COMMUNITY_Community 26|Community 26]]
- [[_COMMUNITY_Community 27|Community 27]]
- [[_COMMUNITY_Community 28|Community 28]]
- [[_COMMUNITY_Community 29|Community 29]]
- [[_COMMUNITY_Community 30|Community 30]]
- [[_COMMUNITY_Community 31|Community 31]]
- [[_COMMUNITY_Community 32|Community 32]]
- [[_COMMUNITY_Community 33|Community 33]]
- [[_COMMUNITY_Community 34|Community 34]]
- [[_COMMUNITY_Community 35|Community 35]]
- [[_COMMUNITY_Community 36|Community 36]]
- [[_COMMUNITY_Community 37|Community 37]]
- [[_COMMUNITY_Community 38|Community 38]]
- [[_COMMUNITY_Community 39|Community 39]]
- [[_COMMUNITY_Community 40|Community 40]]
- [[_COMMUNITY_Community 41|Community 41]]
- [[_COMMUNITY_Community 42|Community 42]]
- [[_COMMUNITY_Community 43|Community 43]]
- [[_COMMUNITY_Community 44|Community 44]]
- [[_COMMUNITY_Community 45|Community 45]]
- [[_COMMUNITY_Community 46|Community 46]]
- [[_COMMUNITY_Community 47|Community 47]]
- [[_COMMUNITY_Community 48|Community 48]]
- [[_COMMUNITY_Community 49|Community 49]]
- [[_COMMUNITY_Community 50|Community 50]]
- [[_COMMUNITY_Community 51|Community 51]]
- [[_COMMUNITY_Community 52|Community 52]]
- [[_COMMUNITY_Community 72|Community 72]]
- [[_COMMUNITY_Community 73|Community 73]]
- [[_COMMUNITY_Community 74|Community 74]]
- [[_COMMUNITY_Community 75|Community 75]]
- [[_COMMUNITY_Community 76|Community 76]]
- [[_COMMUNITY_Community 77|Community 77]]
- [[_COMMUNITY_Community 78|Community 78]]
- [[_COMMUNITY_Community 79|Community 79]]
- [[_COMMUNITY_Community 80|Community 80]]
- [[_COMMUNITY_Community 81|Community 81]]

## God Nodes (most connected - your core abstractions)
1. `assert()` - 28 edges
2. `lookupPath()` - 26 edges
3. `parse_card_html()` - 20 edges
4. `hashes` - 18 edges
5. `run()` - 17 edges
6. `isDir()` - 16 edges
7. `Settings` - 15 edges
8. `run()` - 15 edges
9. `open()` - 15 edges
10. `H()` - 15 edges

## Surprising Connections (you probably didn't know these)
- `test_guest_card()` --calls--> `validate_row()`  [INFERRED]
  tests/test_parsing.py → src/conrad_parser/validation/rules.py
- `test_offers_from_xhr_payload_take_precedence()` --calls--> `parse_card_html()`  [INFERRED]
  tests/test_parsing.py → src/conrad_parser/parsing/product_card.py
- `test_empty_page_is_flagged()` --calls--> `validate_row()`  [INFERRED]
  tests/test_parsing.py → src/conrad_parser/validation/rules.py
- `test_csv_row()` --calls--> `parse_card_html()`  [INFERRED]
  tests/test_parsing.py → src/conrad_parser/parsing/product_card.py
- `test_ean13()` --calls--> `ean13_ok()`  [INFERRED]
  tests/test_validation.py → src/conrad_parser/validation/rules.py

## Communities (90 total, 6 thin omitted)

### Community 0 - "Community 0"
Cohesion: 0.09
Nodes (48): accept_cookies(), choose_business_customer(), collect_links(), dismiss_customer_dialog(), dump_debug(), ean13_ok(), extract_nuxt_payload(), fetch_card() (+40 more)

### Community 1 - "Community 1"
Cohesion: 0.06
Nodes (40): $a(), ab(), ac(), Cd(), Dd(), fc(), Gc(), hc() (+32 more)

### Community 2 - "Community 2"
Cohesion: 0.14
Nodes (33): aa(), B(), c(), D(), ea(), F(), fa(), G() (+25 more)

### Community 3 - "Community 3"
Cohesion: 0.06
Nodes (35): appid, appid, appid, appid, appid, appid, appid, appid (+27 more)

### Community 4 - "Community 4"
Cohesion: 0.08
Nodes (31): expiry, Y, expiry, Y, expiry, Y, expiry, Y (+23 more)

### Community 5 - "Community 5"
Cohesion: 0.04
Nodes (32): allocateUnusedWorker(), analyzePath(), assignWasmImports(), checkUnflushedContent(), done(), EmscriptenEH, EmscriptenSjLj, ExitStatus (+24 more)

### Community 6 - "Community 6"
Cohesion: 0.09
Nodes (30): close(), closeStream(), createStream(), doMsync(), dupStream(), expandFileStorage(), _fd_close(), _fd_read() (+22 more)

### Community 7 - "Community 7"
Cohesion: 0.14
Nodes (32): chdir(), createNode(), destroyNode(), flagsToPermissionString(), hashAddNode(), hashName(), hashRemoveNode(), isBlkdev() (+24 more)

### Community 8 - "Community 8"
Cohesion: 0.16
Nodes (21): establish_session(), Открывает главную и приводит браузер в рабочее состояние: вход в аккаунт,     ес, BaseSettings, Переменные окружения (или файл .env в корне проекта). Обе необязательны:     без, Settings, AuthError, Режим --auth, но войти в аккаунт не получилось., Response (+13 more)

### Community 9 - "Community 9"
Cohesion: 0.29
Nodes (14): Gh(), Hh(), J(), ma(), Mh(), rh(), th(), uh() (+6 more)

### Community 10 - "Community 10"
Cohesion: 0.16
Nodes (23): ca(), af(), b(), bf(), c(), cf(), e(), f() (+15 more)

### Community 11 - "Community 11"
Cohesion: 0.15
Nodes (25): ka(), Ba(), bb(), cb(), db(), eb(), fb(), Fd() (+17 more)

### Community 12 - "Community 12"
Cohesion: 0.12
Nodes (26): Ah(), bg(), cc(), cg(), Ch(), d(), df(), dg() (+18 more)

### Community 13 - "Community 13"
Cohesion: 0.18
Nodes (19): assert(), assignWasmExports(), checkStackCookie(), createExportWrapper(), createStandardStreams(), createWasm(), establishStackSpace(), handleMessage() (+11 more)

### Community 14 - "Community 14"
Cohesion: 0.23
Nodes (13): createDefaultDevices(), createDefaultDirectories(), createDevice(), createPath(), createSpecialDirectories(), EnsureDir(), mkdev(), mkdir() (+5 more)

### Community 15 - "Community 15"
Cohesion: 0.19
Nodes (21): ae(), be(), ce(), de(), ee(), fe(), gd(), ge() (+13 more)

### Community 16 - "Community 16"
Cohesion: 0.22
Nodes (14): calculateAt(), fstat(), getattr(), getStr(), isChrdev(), isDevice(), lstat(), stat() (+6 more)

### Community 17 - "Community 17"
Cohesion: 0.12
Nodes (15): background, service_worker, type, content_security_policy, extension_pages, description, host_permissions, key (+7 more)

### Community 18 - "Community 18"
Cohesion: 0.18
Nodes (15): abort(), checkIncomingModuleAPI(), chmod(), create(), createDataFile(), createFile(), createLazyFile(), forceLoadFile() (+7 more)

### Community 20 - "Community 20"
Cohesion: 0.14
Nodes (16): checkOpExists(), chown(), doChmod(), doChown(), doSetAttr(), doTruncate(), fchmod(), fchown() (+8 more)

### Community 21 - "Community 21"
Cohesion: 0.15
Nodes (12): Human, Имитация действий человека: курсор по кривой Безье, клики, прокрутка, ввод текст, Действия на одной вкладке. Помнит позицию курсора между движениями., Плавное движение курсора по кривой Безье с лёгким дрожанием и разной скоростью., Подвести курсор к элементу, чуть подумать и кликнуть в случайную точку внутри не, Прокрутка неровными порциями, иногда с небольшим возвратом вверх., Несколько случайных движений курсора по странице., float (+4 more)

### Community 22 - "Community 22"
Cohesion: 0.33
Nodes (5): description, manifest_version, name, update_url, version

### Community 24 - "Community 24"
Cohesion: 0.40
Nodes (4): manifest_version, name, preload_data_format, version

### Community 25 - "Community 25"
Cohesion: 0.40
Nodes (4): manifest_version, name, ruleset_format, version

### Community 26 - "Community 26"
Cohesion: 0.16
Nodes (15): is_logged_in(), login(), _open_login_form(), userinfo отвечает 200 только при активной сессии (401 у гостя)., Konto -> Anmelden -> e-mail -> Weiter -> пароль -> Login. Возвращает True при ус, pause(), bool, Human (+7 more)

### Community 27 - "Community 27"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 28 - "Community 28"
Cohesion: 0.67
Nodes (3): main(), recorder.py: ручная запись действий на conrad.de для подбора селекторов.  Запуск, slug()

### Community 29 - "Community 29"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 30 - "Community 30"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 31 - "Community 31"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 32 - "Community 32"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 33 - "Community 33"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 34 - "Community 34"
Cohesion: 0.50
Nodes (3): associatedSites, primary, serviceSites

### Community 35 - "Community 35"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 36 - "Community 36"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 37 - "Community 37"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 38 - "Community 38"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 39 - "Community 39"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 40 - "Community 40"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 41 - "Community 41"
Cohesion: 0.19
Nodes (13): first(), html_to_text(), jsonld(), fmt_attr(), parse_card_html(), Карточка товара: __NUXT_DATA__ + JSON-LD (+ перехваченный XHR с предложениями)., int, str (+5 more)

### Community 42 - "Community 42"
Cohesion: 0.18
Nodes (9): bool, ProductRow, str, test_ean13(), test_rising_price_tiers_flagged(), ean13_ok(), Лёгкая проверка собранной строки. Замечания пишутся в колонку validation_issues., Возвращает список кодов замечаний (пусто = всё в порядке). (+1 more)

### Community 43 - "Community 43"
Cohesion: 0.19
Nodes (11): dump_debug(), HTML и скриншот текущей страницы в debug/ для разбора проблем., wait_cloudflare(), collect_links(), Страница бренда отдаёт 90 товаров; следующие страницы: ?page=N., int, Page, str (+3 more)

### Community 44 - "Community 44"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 45 - "Community 45"
Cohesion: 0.50
Nodes (3): manifest_version, name, version

### Community 46 - "Community 46"
Cohesion: 0.26
Nodes (12): Offer, num(), offers_from_nuxt(), _offers_of(), parse_offer(), parse_offers_payload(), Предложения продавцов: из XHR /api/product/offers или из SSR-состояния (гостевой, Ответ POST /api/product/offers: {"products": [{"productId", "offers", "ineligibl (+4 more)

### Community 47 - "Community 47"
Cohesion: 0.17
Nodes (11): code:bash (cp env.example .env   # и при желании заполнить CONRAD_EMAIL), code:bash (python3 -m venv venv), code:bash (docker compose build), code:block4 (src/), conrad.de parser (Balluff), Запуск без Docker (только Python), Запуск в Docker, Настройка (+3 more)

### Community 49 - "Community 49"
Cohesion: 0.24
Nodes (11): extract_nuxt_payload(), find_with_key(), SSR-состояние Nuxt (<script id="__NUXT_DATA__">) в формате devalue., Формат devalue: значения объектов/массивов это индексы в общем списке., Первый словарь в дереве, у которого есть ключ key., unflatten(), walk(), Any (+3 more)

### Community 50 - "Community 50"
Cohesion: 0.25
Nodes (9): ParserError, Ошибка, после которой продолжать сбор нет смысла., Exception, Namespace, main(), parse_args(), int, str (+1 more)

### Community 51 - "Community 51"
Cohesion: 0.24
Nodes (10): bool, float, int, Path, ProductRow, str, Запись в CSV: списки склеиваются разделителем, сложные поля хранятся как JSON-ст, to_csv_row() (+2 more)

### Community 52 - "Community 52"
Cohesion: 0.33
Nodes (10): Ea(), ib(), le(), nd(), Pd(), Qd(), Rd(), sd() (+2 more)

### Community 72 - "Community 72"
Cohesion: 0.39
Nodes (7): BaseModel, Document, Offer, PriceScale, ProductRow, Схемы строки CSV. Порядок полей ProductRow задаёт порядок колонок., _Schema

### Community 73 - "Community 73"
Cohesion: 0.36
Nodes (7): fetch_card(), Открывает карточку как пользователь и возвращает HTML и ответ XHR с предложениям, Собирает и проверяет карточку. Если есть критичные замечания (страница могла, scrape_product(), Human, ProductRow, str

### Community 74 - "Community 74"
Cohesion: 0.39
Nodes (7): Human, Locator, _business_button(), choose_business_customer(), dismiss_customer_dialog(), Окно выбора типа клиента (Privatkunde / Geschäftskunde)., Если окно показано, выбираем Geschäftskunde (при входе роль всё равно     опреде

### Community 75 - "Community 75"
Cohesion: 0.62
Nodes (7): oa(), pa(), qa(), ta(), ua(), va(), wa()

### Community 76 - "Community 76"
Cohesion: 0.43
Nodes (5): build_card_html(), card_html(), devalue_flatten(), str, Обратное к parsing.nuxt.unflatten: значения объектов/массивов заменяются индекса

### Community 77 - "Community 77"
Cohesion: 0.50
Nodes (3): open_browser(), Настоящий Chrome с постоянным профилем: cookie и сессия переживают перезапуск., Page

### Community 78 - "Community 78"
Cohesion: 0.67
Nodes (3): _both_or_none(), has_credentials(), bool

## Knowledge Gaps
- **143 isolated node(s):** `docker-entrypoint.sh script`, `DISPLAY`, `Human`, `int`, `str` (+138 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `parse_card_html()` connect `Community 41` to `Community 72`, `Community 73`, `Community 42`, `Community 46`, `Community 49`, `Community 50`, `Community 51`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **Why does `scrape_product()` connect `Community 73` to `Community 8`, `Community 41`, `Community 42`, `Community 26`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `run()` connect `Community 8` to `Community 73`, `Community 43`, `Community 77`, `Community 80`, `Community 50`, `Community 51`, `Community 26`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Are the 16 inferred relationships involving `parse_card_html()` (e.g. with `test_guest_card()` and `test_offers_from_xhr_payload_take_precedence()`) actually correct?**
  _`parse_card_html()` has 16 INFERRED edges - model-reasoned connections that need verification._
- **Are the 11 inferred relationships involving `run()` (e.g. with `main()` and `AuthError`) actually correct?**
  _`run()` has 11 INFERRED edges - model-reasoned connections that need verification._
- **What connects `recorder.py: ручная запись действий на conrad.de для подбора селекторов.  Запуск`, `docker-entrypoint.sh script`, `DISPLAY` to the rest of the system?**
  _193 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.08549019607843138 - nodes in this community are weakly interconnected._