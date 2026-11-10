import json

import pytest


def devalue_flatten(obj) -> list:
    """Inverse of parsing.nuxt.unflatten: object/array values are replaced with indexes."""
    table: list = []

    def add(v):
        i = len(table)
        table.append(None)
        if isinstance(v, dict):
            table[i] = {k: add(x) for k, x in v.items()}
        elif isinstance(v, list):
            table[i] = [add(x) for x in v]
        else:
            table[i] = v
        return i

    add(obj)
    return table


def _offer(seller, price, stock, scales):
    return {
        "sellerName": seller, "sellerId": "S1", "offerId": f"O-{seller}",
        "minimumOrderQuantity": 1, "multiplier": None,
        "price": {"unitPrice": price, "minShippingCosts": 5.95, "freeShipping": False,
                  "priceScales": [{"scaleFrom": q, "pricePerUnit": p} for q, p in scales]},
        "availability": {"stockQuantity": stock, "availabilityState": "AVAILABLE",
                         "promisedDeliveryDate": "2026-11-14"},
    }


PRODUCT = {
    "shortProductNumber": "2471385",
    "productShortInformation": {"title": "Balluff BES000H Induktiver Sensor"},
    "productImages": [{"imageUrl": "https://asset.conrad.com/a.jpg"},
                      {"imageUrl": "https://asset.conrad.com/b.jpg"}],
    "productMedia": {"manuals": [
        {"typeName": "Datenblatt", "language": "en", "title": "DS en",
         "fullUrl": "https://asset.conrad.com/ds_en.pdf"},
        {"typeName": "Datenblatt", "language": "de", "title": "DS de",
         "fullUrl": "https://asset.conrad.com/ds_de.pdf"},
    ]},
    "productFullInformation": {
        "eanCode": "4030664105465",
        "manufacturer": {"id": "BES 516-300-S135-S4-D"},
        "headline": "Induktiver Näherungsschalter",
        "features": ["IO-Link", "IP67"],
        "description": "<p>Beschreibung</p>",
        "technicalAttributes": [
            {"attributeName": "Produkt-Art", "values": [{"value": "Induktiver Sensor"}]},
            {"attributeName": "Betriebsspannung max.",
             "values": [{"value": 30, "unit": {"name": "V/DC"}}]},
            {"attributeName": "Kontaktart", "values": [{"value": "Schließer"}]},
            {"attributeName": "Schaltabstand (max.)",
             "values": [{"value": 2, "unit": {"name": "mm"}}]},
            {"attributeName": "Ausgänge", "values": [{"value": "PNP"}]},
        ],
    },
}

OFFERS = {
    "eligibleOffers": [_offer("Conrad Electronic", 42.5, 7, [(1, 42.5), (10, 40.0)])],
    "ineligibleOffers": [_offer("Other Seller", 45.0, None, [(1, 45.0)])],
}


def build_card_html(product=PRODUCT, offers=OFFERS) -> str:
    nuxt = devalue_flatten({"data": {"pdp": product, "offers": offers}})
    crumbs = {"itemListElement": [{"name": "Startseite"}, {"name": "Sensorik"},
                                  {"name": "Induktive Sensoren"}]}
    return (
        "<html><head>"
        f'<script type="application/ld+json" data-hid="pdp-breadcrumb-ld">{json.dumps(crumbs)}</script>'
        "</head><body><h1>Balluff Sensor</h1>"
        "<div>Bestell-Nr.: 2471385 - 62</div>"
        "<div>Hinweise Bitte beachten Sie die Montagehinweise des Herstellers. Beschreibung</div>"
        "<div>Verkauf durch Conrad Electronic Versand durch Conrad Electronic Menge</div>"
        f'<script type="application/json" id="__NUXT_DATA__">{json.dumps(nuxt)}</script>'
        "</body></html>"
    )


CARD_URL = "https://www.conrad.de/de/p/balluff-bes000h-induktiver-sensor-2471385.html"


@pytest.fixture
def card_html() -> str:
    return build_card_html()
