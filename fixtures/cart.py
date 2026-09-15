from typing import Generator

import pytest
from pydantic import BaseModel

from clients.cart_client.cart_schema import AddCartRequestSchema, CartResponseSchema
from clients.http_clients import HttpClients
from fixtures.users import FunctionUser


class FunctionCart(BaseModel):
    """
    Модель для агрегации данных фикстуры function_cart
    """

    request: AddCartRequestSchema
    response: CartResponseSchema

    @property
    def product_id(self):
        return self.request.product_id

    @property
    def incorrect_product_id(self):
        return self.request.product_id[::-3] + "qqw"


@pytest.fixture(scope="function")
def product_to_cart() -> AddCartRequestSchema:
    return AddCartRequestSchema(
        product_id="550e8400-e29b-41d4-a716-446655440001", quantity=1
    )


@pytest.fixture(scope="function")
def product_over_stock_request() -> AddCartRequestSchema:
    return AddCartRequestSchema(
        product_id="550e8400-e29b-41d4-a716-446655440001", quantity=99999
    )


@pytest.fixture(scope="function")
def function_cart(
    http: HttpClients, function_user: FunctionUser, product_to_cart
) -> Generator[FunctionCart, None, None]:
    """
    Фикстура для создания корзины с товаром
    :param product_to_cart:
    :param http:
    :param function_user:
    :return:
    """
    request = product_to_cart
    cart = http.cart_client.add_product_to_cart(
        function_user.id, request.model_dump(), function_user.access_token
    )
    response = CartResponseSchema.model_validate_json(cart.text)
    yield FunctionCart(request=request, response=response)
    http.cart_client.remove_product_from_cart(
        function_user.id, request.product_id, function_user.access_token
    )
