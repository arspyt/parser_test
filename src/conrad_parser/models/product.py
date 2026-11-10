"""CSV row schemas. The field order of ProductRow defines the column order."""
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

SessionMode = Literal["auth", "guest"]
Number = int | float

KEY_SPECS = ("Produkt-Art", "Betriebsspannung max.", "Kontaktart",
             "Schaltabstand (max.)", "Ausgänge")


class _Schema(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)


class PriceScale(_Schema):
    qty: Number | None = None
    price_per_unit: float | None = None
    saved_percent: Number | None = None
    saved_amount: Number | None = None


class Offer(_Schema):
    seller: str | None = None
    seller_id: str | None = None
    offer_id: str | None = None
    unit_price_net: float | None = None
    shipping: float | None = None
    free_shipping: bool | None = None
    stock: int | None = None
    availability_state: str | None = None
    delivery_date: str | None = None
    min_order_qty: int | None = None
    multiplier: int | None = None
    fits_requested_qty: bool = True
    price_scales: list[PriceScale] = []


class Document(_Schema):
    language: str | None = None
    title: str | None = None
    url: str | None = None


class ProductRow(_Schema):
    model_config = ConfigDict(coerce_numbers_to_str=True,
                              validate_by_name=True, validate_by_alias=True)

    url: str
    product_id: str = ""
    title: str = ""
    breadcrumbs: list[str] = []
    image_urls: list[str] = []
    ean: str = ""
    manufacturer_part_no: str = ""
    order_no: str = ""

    produkt_art: str = Field("", alias="Produkt-Art")
    betriebsspannung_max: str = Field("", alias="Betriebsspannung max.")
    kontaktart: str = Field("", alias="Kontaktart")
    schaltabstand_max: str = Field("", alias="Schaltabstand (max.)")
    ausgaenge: str = Field("", alias="Ausgänge")
    tech_data: dict[str, str] = {}

    datasheet_url: str = ""
    documents: dict[str, list[Document]] = {}

    highlights: str = ""
    description: str = ""
    notes: str = ""

    offers_count: int = 0
    offers: list[Offer] = []
    shipped_by: str = ""
    sold_by: str = ""
    stock: int | None = None
    delivery_date: str | None = None
    total_price_net: float | None = None
    shipping: float | None = None
    price_tiers: list[PriceScale] = []

    session_mode: SessionMode | None = None
    validation_issues: list[str] = []
