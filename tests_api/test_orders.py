from http import HTTPStatus

import pytest

from assertions.base_assert import assert_status_code
from assertions.order_asserts import (
    assert_create_order_id_is_note_none,
    assert_order_fields,
    assert_order_id_is_correct,
    assert_order_price_sum_is_correct,
    assert_order_status,
    user_id_is_correct,
)
from clients.http_clients import HttpClients
from clients.order_client.order_schema import (
    CreateOrderResponseSchema,
    CreateOrderSchema,
    GetOrderListSchema,
    RefreshOrderSchema,
)
from fixtures.cart import FunctionCart
from fixtures.order import FunctionOrder
from fixtures.users import FunctionUser

@pytest.mark.orders
class TestOrders:

    def test_create_order(
        self,
        http: HttpClients,
        function_user: FunctionUser,
        function_cart: FunctionCart,
    ):
        """
        Проверка создания заказа
        :param http: Клиент для запроса
        :param function_user: фикстура создающая пользователя
        :param function_cart:фикстура создающая заказ
        """
        request = CreateOrderSchema(user_id=function_user.id)
        response = http.order_client.create_order(request, function_user.access_token)
        assert_status_code(response, HTTPStatus.OK)
        response_data = CreateOrderResponseSchema.model_validate_json(response.text)
        assert_order_status(response_data.order, "ORDER_STATUS_CREATED")
        assert_create_order_id_is_note_none(response_data.order)
        assert_order_price_sum_is_correct(response_data.order)
        user_id_is_correct(response_data.order, function_user.id)

    def test_create_order_with_incorrect_user_id(
        self,
        http: HttpClients,
        function_user: FunctionUser,
        function_cart: FunctionCart,
    ):
        """
        Создание заказа с некорректным id пользователя
        :param http: Клиент для запроса
        :param function_user: фикстура создающая пользователя
        :param function_cart: фикстура создающая корзину
        """
        data = CreateOrderSchema(user_id=function_user.incorrect_id)
        response = http.order_client.create_order(data, function_user.access_token)
        assert_status_code(response, HTTPStatus.FORBIDDEN)

    def test_get_order(
        self,
        http: HttpClients,
        function_order: FunctionOrder,
        function_user: FunctionUser,
    ):
        """
        Получение заказа
        :param http: Клиент для запроса
        :param function_order: фикстура создающая заказ
        :param function_user: фикстура создающая пользователя
        """
        order_id = function_order.get_order_id()
        response = http.order_client.get_order(order_id, function_user.access_token)
        assert_status_code(response, HTTPStatus.OK)
        response_data = CreateOrderResponseSchema.model_validate_json(response.text)
        assert_order_id_is_correct(response_data.order, order_id)
        assert_order_price_sum_is_correct(response_data.order)
        assert_order_status(response_data.order, "ORDER_STATUS_CREATED")
        user_id_is_correct(response_data.order, function_user.id)

    def test_get_order_list(
        self,
        http: HttpClients,
        function_order: FunctionOrder,
        function_user: FunctionUser,
    ):
        """
        Получения списка заказов
        :param http: Клиент для запроса
        :param function_order: фикстура создающая заказ
        :param function_user: фикстура создающая пользователя
        """
        response = http.order_client.get_orders(
            function_user.id, function_user.access_token
        )
        assert_status_code(response, HTTPStatus.OK)
        response_data = GetOrderListSchema.model_validate_json(response.text)
        for order in response_data.orders:
            assert_order_fields(order, function_user.id)

    def test_cansel_order(
        self,
        http: HttpClients,
        function_order: FunctionOrder,
        function_user: FunctionUser,
    ):
        """
        Отмена заказа
        :param http: Клиент для запроса
        :param function_order: фикстура создающая заказ
        :param function_user: фикстура создающая пользователя
        """
        order_id = function_order.get_order_id()
        response = http.order_client.cancel_order(
            order_id, function_user.access_token
        )
        assert_status_code(response, HTTPStatus.OK)
        assert_order_status(function_order.response.order, "ORDER_STATUS_CREATED")
        response_data = CreateOrderResponseSchema.model_validate_json(response.text)
        assert_order_status(response_data.order, "ORDER_STATUS_CANCELLED")

    def test_refresh_status(
        self,
        http: HttpClients,
        function_order: FunctionOrder,
        function_user: FunctionUser,
        update_order_status_request: RefreshOrderSchema,
    ):
        """
        Обновление статуса заказа
        :param http: Клиент для запроса
        :param function_order: фикстура создающая заказ
        :param function_user: фикстура создающая пользователя
        :param update_order_status_request:
        """
        order_id = function_order.get_order_id()
        response = http.order_client.refresh_order(
            order_id,
            update_order_status_request,
            function_user.access_token,
        )
        assert_status_code(response, HTTPStatus.OK)
        assert_order_status(function_order.response.order, "ORDER_STATUS_CREATED")
        response_data = CreateOrderResponseSchema.model_validate_json(response.text)
        assert_order_status(response_data.order, "ORDER_STATUS_PAID")
