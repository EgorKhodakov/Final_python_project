from typing import List

from pydantic import BaseModel, Field


class PromocodeSchema(BaseModel):
    code: str


class AddCartRequestSchema(BaseModel):
    """
    Модель товара расположенного в корзине
    """

    product_id: str = Field(alias="productId")
    quantity: int


class CartResponseSchema(BaseModel):
    """
    Модель ответа запроса на получение корзины
    """

    items: List[AddCartRequestSchema]
    total_price_cents: str = Field(alias="totalPriceCents")
    subtotal_cents: str = Field(alias="subtotalCents")
    discount_cents: str = Field(alias="discountCents")
    applied_promocode: str = Field(alias="appliedPromocode")
    combo_discount_applied: bool = Field(alias="comboDiscountApplied")
    expires_at: str = Field(alias="expiresAt")
