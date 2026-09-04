from typing import List

from pydantic import BaseModel, Field


class CreateOrderSchema(BaseModel):
    """
    Модель создания заказа
    """

    user_id: str


class RefreshOrderSchema(BaseModel):
    """
    Модель обновления заказа
    """

    from_status: str = Field(alias="fromStatus")
    to_status: str = Field(alias="toStatus")


class OrderItemSchema(BaseModel):
    """ """

    product_id: str = Field(alias="productId")
    quantity: int
    price_cents: str = Field(alias="priceCents")


class OrderSchema(BaseModel):
    """
    Базовая модель заказа
    """

    id: str
    user_id: str = Field(alias="userId")
    items: List[OrderItemSchema]
    total_amount_cents: str = Field(alias="totalAmountCents")
    status: str


class GetOrderListSchema(BaseModel):
    """
    Схема ответа на получение списка заказов
    """
    orders: List[OrderSchema]

class CreateOrderResponseSchema(BaseModel):
    """
    Схема ответа на создание заказа
    """

    order: OrderSchema
