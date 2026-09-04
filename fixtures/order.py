import pytest

from clients.http_clients import HttpClients
from clients.order_client.order_schema import (
    CreateOrderResponseSchema,
    CreateOrderSchema, RefreshOrderSchema,
)
from fixtures.cart import FunctionCart
from fixtures.users import FunctionUser


@pytest.fixture(scope="function")
def function_order(
    http: HttpClients, function_user: FunctionUser, function_cart: FunctionCart
) -> CreateOrderResponseSchema:
    """
    Фикстура для создания заказа
    :param http:
    :param function_user:
    :param function_cart:
    :return:
    """
    data = CreateOrderSchema(user_id=function_user.id())
    response = http.order_client.create_order(data, function_user.access_token())
    return CreateOrderResponseSchema.model_validate_json(response.text)

@pytest.fixture(scope="function")
def update_order_status_request() -> RefreshOrderSchema:
    request = RefreshOrderSchema(
        fromStatus="ORDER_STATUS_CREATED",
        toStatus="ORDER_STATUS_PAID",
    )
    return request