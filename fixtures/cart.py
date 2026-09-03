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

    def product_id(self):
        return self.request.product_id

    def user_id(self):
        return self.request.user_id


@pytest.fixture(scope="function")
def get_cart(http: HttpClients, function_user: FunctionUser):
    response = http.cart_client.get_cart(
        function_user.id(), function_user.access_token()
    )
    return response


@pytest.fixture(scope="function")
def function_cart(
    http: HttpClients, function_user: FunctionUser, get_cart
) -> Generator[FunctionCart, None, None]:
    """
    Фикстура для создания корзины с товаром
    :param http:
    :param function_user:
    :param get_cart:
    :return:
    """
    request = AddCartRequestSchema(
        productId="550e8400-e29b-41d4-a716-446655440001",
        quantity=1,
    )
    cart = http.cart_client.add_product_to_cart(
        function_user.id(), request.model_dump(), function_user.access_token()
    )
    response = CartResponseSchema.model_validate_json(cart.text)
    yield FunctionCart(request=request, response=response)
    http.cart_client.remove_product_from_cart(
        function_user.id(), request.product_id, function_user.access_token()
    )
