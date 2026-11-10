"""Seller offers: from the /api/product/offers XHR or from the SSR state (guest mode)."""
from typing import Any

from conrad_parser.models import Offer, PriceScale
from conrad_parser.parsing.nuxt import find_with_key


def num(x: Any) -> float | None:
    return float(x) if isinstance(x, (int, float)) else None


def parse_offer(of: dict, is_eligible: bool) -> Offer:
    pr, av = of.get("price") or {}, of.get("availability") or {}
    scales = []
    base = None
    for s in pr.get("priceScales") or []:
        ppu = num(s.get("pricePerUnit"))
        if base is None:
            base = ppu
        qty = s.get("scaleFrom")
        pct = s.get("savedPercentage")
        saved = s.get("savedAmount")
        if base and ppu is not None and (pct is None or saved is None):
            pct = round((1 - ppu / base) * 100)
            saved = round((base - ppu) * qty, 2)
        scales.append(PriceScale(qty=qty, price_per_unit=ppu,
                                 saved_percent=pct, saved_amount=saved))
    return Offer(
        seller=of.get("sellerName"),
        seller_id=of.get("sellerId"),
        offer_id=of.get("offerId"),
        unit_price_net=num(pr.get("unitPrice")),
        shipping=num(pr.get("minShippingCosts")),
        free_shipping=pr.get("freeShipping"),
        stock=av.get("stockQuantity") if av.get("isShowStock", True) else None,
        availability_state=av.get("availabilityState"),
        delivery_date=av.get("promisedDeliveryDate"),
        min_order_qty=of.get("minimumOrderQuantity"),
        multiplier=of.get("multiplier"),
        fits_requested_qty=is_eligible,
        price_scales=scales,
    )


def _offers_of(eligible: list | None, ineligible: list | None) -> list[Offer]:
    return ([parse_offer(o, True) for o in eligible or []] +
            [parse_offer(o, False) for o in ineligible or []])


def parse_offers_payload(payload: dict | None, product_id: str) -> list[Offer]:
    """Response of POST /api/product/offers: {"products": [{"productId", "offers", "ineligibleOffers"}]}."""
    for pr in (payload or {}).get("products", []):
        if str(pr.get("productId", "")).lstrip("0") == str(product_id).lstrip("0"):
            return _offers_of(pr.get("offers"), pr.get("ineligibleOffers"))
    return []


def offers_from_nuxt(data: Any) -> list[Offer]:
    coll = find_with_key(data, "eligibleOffers")
    return _offers_of(coll.get("eligibleOffers"), coll.get("ineligibleOffers")) if coll else []
