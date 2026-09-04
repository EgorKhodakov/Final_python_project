from assertions.base_assert import assert_status_code
from assertions.order_asserts import assert_order_status, assert_order_price_sum, \
    assert_create_order_id_is_note_none, assert_order_id_is_correct, user_id_is_correct, assert_order_fields
from clients.http_clients import HttpClients
from clients.order_client.order_schema import (
    CreateOrderResponseSchema,
    CreateOrderSchema,
    RefreshOrderSchema, GetOrderListSchema,
)
from fixtures.cart import FunctionCart
from fixtures.users import FunctionUser


def test_create_order(
    http: HttpClients, function_user: FunctionUser, function_cart: FunctionCart
):
    """
    Проверка создания заказа
    :param http:
    :param function_user:
    :param function_cart:
    :return:
    """
    data = CreateOrderSchema(user_id=function_user.id())
    response = http.order_client.create_order(data, function_user.access_token())
    assert_status_code(response, 200)
    response_data = CreateOrderResponseSchema.model_validate_json(response.text)
    assert_order_status(response_data.order, "ORDER_STATUS_CREATED")
    assert_create_order_id_is_note_none(response_data.order)
    assert_order_price_sum(response_data.order)
    user_id_is_correct(response_data.order, function_user.id())


def test_create_order_with_incorrect_id(
    http: HttpClients, function_user: FunctionUser, function_cart: FunctionCart
):
    data = CreateOrderSchema(user_id="f134a6ec-3879-4c51-8958-b3a6df7e444c")
    response = http.order_client.create_order(data, function_user.access_token())
    assert_status_code(response, 403)


def test_get_order(
    http: HttpClients,
    function_order: CreateOrderResponseSchema,
    function_user: FunctionUser,
):
    order_id = function_order.order.id
    response = http.order_client.get_order(
        function_order.order.id, function_user.access_token()
    )
    assert_status_code(response, 200)
    response_data = CreateOrderResponseSchema.model_validate_json(response.text)
    assert_order_id_is_correct(response_data.order, order_id)
    assert_order_price_sum(response_data.order)
    assert_order_status(response_data.order, "ORDER_STATUS_CREATED")
    user_id_is_correct(response_data.order, function_user.id())


def test_get_order_list(
    http: HttpClients,
    function_order: CreateOrderResponseSchema,
    function_user: FunctionUser,
):
    response = http.order_client.get_orders(
        function_user.id(), function_user.access_token()
    )
    assert_status_code(response, 200)
    response_data = GetOrderListSchema.model_validate_json(response.text)
    for order in response_data.orders:
        assert_order_fields(order, function_user.id())



def test_cansel_order(
    http: HttpClients,
    function_order: CreateOrderResponseSchema,
    function_user: FunctionUser,
):
    response = http.order_client.cancel_order(
        function_order.order.id, function_user.access_token()
    )
    assert_status_code(response, 200)
    assert_order_status(function_order.order, "ORDER_STATUS_CREATED")
    response_data = CreateOrderResponseSchema.model_validate_json(response.text)
    assert_order_status(response_data.order, "ORDER_STATUS_CANCELLED")




def test_refresh_status(
    http: HttpClients,
    function_order: CreateOrderResponseSchema,
    function_user: FunctionUser,
    update_order_status_request: RefreshOrderSchema,
):
    response = http.order_client.refresh_order(
        function_order.order.id, update_order_status_request, function_user.access_token()
    )
    assert_status_code(response, 200)
    assert_order_status(function_order.order, "ORDER_STATUS_CREATED")
    response_data = CreateOrderResponseSchema.model_validate_json(response.text)
    assert_order_status(response_data.order, "ORDER_STATUS_PAID")

