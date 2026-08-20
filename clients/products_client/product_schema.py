from typing import List

from pydantic import BaseModel, Field


class ProductShema(BaseModel):
    """
    Модель продукта
    """

    id: str
    name: str
    description: str
    price_cents: str = Field(alias="priceCents")
    brand: str


class ProductListSchema(BaseModel):
    """
    Модель получения списка продуктов
    """

    products: List[ProductShema]
    next_page_Token: str = Field(alias="nextPageToken")
