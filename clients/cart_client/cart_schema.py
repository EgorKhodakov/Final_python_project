from typing import List

from pydantic import BaseModel


class PromocodeSchema(BaseModel):
    code: str


class AddCartRequestSchema(BaseModel):
    """
    Модель товара расположенного в корзине
    """

    productId: str
    quantity: int


class CartResponseSchema(BaseModel):
    """
    Модель ответа запроса на получение корзины
    """

    items: List[AddCartRequestSchema]
    totalPriceCents: str
    subtotalCents: str
    discountCents: str
    appliedPromocode: str
    comboDiscountApplied: bool
    expiresAt: str
