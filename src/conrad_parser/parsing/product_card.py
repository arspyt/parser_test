"""Product page: __NUXT_DATA__ + JSON-LD (+ the intercepted offers XHR)."""
from conrad_parser.models import KEY_SPECS, Document, ProductRow
from conrad_parser.parsing.html_utils import first, html_to_text, jsonld
from conrad_parser.parsing.nuxt import extract_nuxt_payload, find_with_key, unflatten
from conrad_parser.parsing.offers import offers_from_nuxt, parse_offers_payload


def fmt_attr(attr: dict) -> str:
    parts = []
    for v in attr.get("values") or []:
        s = str(v.get("value", ""))
        unit = (v.get("unit") or {}).get("name")
        parts.append(f"{s} {unit}".strip() if unit else s)
    return ", ".join(parts)


def parse_card_html(html: str, url: str = "", offers_payload: dict | None = None) -> ProductRow:
    data = unflatten(extract_nuxt_payload(html) or [None])
    text = html_to_text(html)

    prod = (find_with_key(data, "productFullInformation") if data else None) or {}
    full = prod.get("productFullInformation") or {}
    short = prod.get("productShortInformation") or {}
    media = prod.get("productMedia") or {}

    product_id = prod.get("shortProductNumber") or first(r"-(\d+)\.html", url)
    crumbs = jsonld(html, "pdp-breadcrumb-ld") or {}

    # --- technical data
    specs = {a["attributeName"]: fmt_attr(a)
             for a in full.get("technicalAttributes") or [] if a.get("attributeName")}

    # --- documents
    docs: dict[str, list[Document]] = {}
    for m in media.get("manuals") or []:
        docs.setdefault(m.get("typeName") or "Dokument", []).append(
            Document(language=m.get("language"), title=m.get("title"), url=m.get("fullUrl")))
    sheets = docs.get("Datenblatt", [])
    datasheet = next((d.url for d in sheets if d.language == "de"),
                     sheets[0].url if sheets else "")

    # --- seller offers
    offers = parse_offers_payload(offers_payload, product_id) if offers_payload else []
    if not offers:                      # guest mode: offers are already in the SSR state
        offers = offers_from_nuxt(data)
    best = offers[0] if offers else None

    feats = full.get("features") or []
    return ProductRow.model_validate({
        "url": url,
        "product_id": product_id,
        "title": short.get("title") or first(r"<h1[^>]*>(.*?)</h1>", html),
        "breadcrumbs": [e.get("name", "") for e in crumbs.get("itemListElement", [])],
        "image_urls": [i.get("imageUrl", "") for i in prod.get("productImages") or []],
        "ean": full.get("eanCode") or first(r"EAN:\s*(\d+)", text),
        "manufacturer_part_no": (full.get("manufacturer") or {}).get("id")
        or first(r"Hst\.-Teile-Nr\.:\s*(\S+)", text),
        "order_no": first(r"Bestell-Nr\.:\s*(\d+(?:\s*-\s*\d+)?)", text) or product_id,
        **{k: specs.get(k, "") for k in KEY_SPECS},
        "tech_data": specs,
        "datasheet_url": datasheet or "",
        "documents": docs,
        "highlights": ((full.get("headline") or "") + "\n" + "\n".join(feats)).strip(),
        "description": full.get("description") or "",
        "notes": first(r"Hinweise\s+(.{20,900}?)\s+Beschreibung", text),
        "offers_count": len(offers),
        "offers": offers,
        "shipped_by": (best and best.seller) or first(r"Versand durch\s+(.+?)\s+Menge", text),
        "sold_by": first(r"Verkauf durch\s+(.+?)\s+Versand durch", text) or "Conrad Electronic",
        "stock": best.stock if best else None,
        "delivery_date": best.delivery_date if best else None,
        "total_price_net": best.unit_price_net if best else None,
        "shipping": best.shipping if best else None,
        "price_tiers": best.price_scales if best else [],
    })
