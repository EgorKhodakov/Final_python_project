from typing import List

from pydantic import BaseModel


class ProductShema(BaseModel):
    """
    Модель продукта
    """

    id: str
    name: str
    description: str
    priceCents: str
    brand: str


class ProductListSchema(BaseModel):
    """
    Модель получения списка продуктов
    """

    products: List[ProductShema]
    nextPageToken: str
