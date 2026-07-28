from typing import List

from pydantic import BaseModel


class PromocodeSchema(BaseModel):
    code: str


class CartSchema(BaseModel):
    """
    Модель товара расположенного в корзине
    """
    product_id: int
    quantity: int


class CartResponseSchema(BaseModel):
    """
    Модель ответа запроса на получение корзины
    """
    items: List[CartSchema]
    totalPriceCents: str
    subtotalCents: str
    discountCents: str
    appliedPromocode: str
    comboDiscountApplied: bool
    expiresAt: str
