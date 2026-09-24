from typing import Generator

import pytest
from pydantic import BaseModel

from clients.http_clients import HttpClients
from clients.order_client.order_schema import (
    CreateOrderResponseSchema,
    CreateOrderSchema,
    RefreshOrderSchema,
)
from fixtures.cart import FunctionCart
from fixtures.users import FunctionUser


class FunctionOrder(BaseModel):

    request: CreateOrderSchema
    response: CreateOrderResponseSchema

    def get_order_id(self):
        return self.response.order.id

    def order_status(self):
        return self.response.order


@pytest.fixture(scope="function")
def function_order(
    http: HttpClients, function_user: FunctionUser, function_cart: FunctionCart
) -> Generator[FunctionOrder, None, None]:
    """
    Фикстура для создания заказа
    :param http:
    :param function_user:
    :param function_cart:
    :return:
    """
    request = CreateOrderSchema(user_id=function_user.id)
    order = http.order_client.create_order(request, function_user.access_token)
    response = CreateOrderResponseSchema.model_validate_json(order.text)
    yield FunctionOrder(request=request, response=response)
    http.order_client.delete_order(request, response.order.id)


@pytest.fixture(scope="function")
def update_order_status_request() -> RefreshOrderSchema:
    request = RefreshOrderSchema(
        fromStatus="ORDER_STATUS_CREATED",
        toStatus="ORDER_STATUS_PAID",
    )
    return request
