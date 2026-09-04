from typing import List

from pydantic import BaseModel, Field, ConfigDict


class ProductShema(BaseModel):
    """
    Модель продукта
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str
    name: str
    description: str
    price_cents: str = Field(alias="priceCents")
    stock_quantity: int = Field(alias="stockQuantity")
    brand: str


class ProductResponseSchema(BaseModel):
    """ """

    product: ProductShema


class ProductListSchema(BaseModel):
    """
    Модель получения списка продуктов
    """

    model_config = ConfigDict(populate_by_name=True)

    products: List[ProductShema]
    next_page_Token: str | None = Field(alias="nextPageToken")
