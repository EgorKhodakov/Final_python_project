import pytest

from clients.http_clients import HttpClients
from clients.order_client.order_schema import (CreateOrderSchema,
                                               OrderResponseSchema)
from fixtures.cart import FunctionCart
from fixtures.users import FunctionUser


@pytest.fixture(scope="function")
def function_order(
    http: HttpClients, function_user: FunctionUser, function_cart: FunctionCart
) -> OrderResponseSchema:
    data = CreateOrderSchema(user_id=function_user.id())
    response = http.order_client.create_order(data, function_user.access_token())
    return OrderResponseSchema.model_validate_json(response.text)
