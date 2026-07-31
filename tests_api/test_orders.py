import pytest

from clients.http_clients import HttpClients
from clients.order_client.order_schema import CreateOrderSchema, OrderResponseSchema, RefreshOrderSchema
from fixtures.cart import FunctionCart
from fixtures.users import FunctionUser


def test_create_order(http: HttpClients, function_user: FunctionUser, function_cart: FunctionCart):
    data = CreateOrderSchema(
       user_id=function_user.id()
   )
    response = http.order_client.create_order(data, function_user.access_token())
    assert response.status_code == 200


def test_create_order_with_incorrect_id(http: HttpClients, function_user: FunctionUser, function_cart: FunctionCart):
    data = CreateOrderSchema(
       user_id="f134a6ec-3879-4c51-8958-b3a6df7e444c"
   )
    response = http.order_client.create_order(data, function_user.access_token())
    assert response.status_code == 403


def test_get_order(http: HttpClients, function_order: OrderResponseSchema, function_user: FunctionUser):
    response = http.order_client.get_orders(function_order.order.id, function_user.access_token())
    assert response.status_code == 200


def test_get_order_success(http: HttpClients, function_order: OrderResponseSchema, function_user: FunctionUser):
    response = http.order_client.get_orders(function_order.order.id, function_user.access_token())
    assert response.status_code == 200


def test_cansel_order(http: HttpClients, function_order: OrderResponseSchema, function_user: FunctionUser):
    response = http.order_client.cancel_order(function_order.order.id, function_user.access_token())
    assert response.status_code == 200


def test_refresh_status(http: HttpClients, function_order: OrderResponseSchema, function_user: FunctionUser):
    request = RefreshOrderSchema(
        fromStatus="ORDER_STATUS_CREATED",
        toStatus="ORDER_STATUS_PAID",
    )
    response = http.order_client.refresh_order(function_order.order.id, request, function_user.access_token())
    assert response.status_code == 200

