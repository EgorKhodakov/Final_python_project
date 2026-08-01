from typing import List

from pydantic import BaseModel


class CreateOrderSchema(BaseModel):
    user_id: str


class RefreshOrderSchema(BaseModel):
    fromStatus: str
    toStatus: str


class OrderItemSchema(BaseModel):
    productId: str
    quantity: int
    priceCents: str


class OrderSchema(BaseModel):
    id: str
    userId: str
    items: List[OrderItemSchema]
    totalAmountCents: str
    status: str


class OrderResponseSchema(BaseModel):
    order: OrderSchema
