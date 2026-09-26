from http import HTTPStatus

import pytest

from assertions.base_assert import assert_equals, assert_status_code
from assertions.cart_asserts import (
    assert_add_product_id_and_quantity,
    assert_cart_fields,
    assert_cart_is_clear,
    assert_product_in_cart,
    assert_product_not_in_cart_db,
    assert_cart_is_clear_db,
)
from clients.cart_client.cart_schema import AddCartRequestSchema, CartResponseSchema
from clients.http_clients import HttpClients
from db_clients.database_facade import FacadeDB
from fixtures.cart import FunctionCart
from fixtures.users import FunctionUser


@pytest.mark.cart
class TestCart:

    def test_get_cart(self, http: HttpClients, function_user: FunctionUser):
        """
        Получение корзины пользователя
        :param http: Клиент для запроса
        :param function_user: фикстура создающая пользователя
        """
        response = http.cart_client.get_cart(
            function_user.id, function_user.access_token
        )
        assert_status_code(response, HTTPStatus.OK)
        assert_cart_fields(response)

    def test_add_product_to_cart(
        self,
        http: HttpClients,
        function_user: FunctionUser,
        product_to_cart: AddCartRequestSchema,
        data_base: FacadeDB,
    ):
        """
        Добавление товара в корзину
        :param http: Клиент для запроса
        :param function_user: фикстура создающая пользователя
        :param product_to_cart: фикстура с параметрами продукта
        """
        request = product_to_cart
        response = http.cart_client.add_product_to_cart(
            function_user.id, request.model_dump(), function_user.access_token
        )
        response_data = CartResponseSchema.model_validate_json(response.text)
        assert_status_code(response, HTTPStatus.OK)
        assert_add_product_id_and_quantity(response_data, request)
        assert_product_in_cart(function_user.id, request.product_id, data_base)

    def test_delete_product_from_cart(
        self,
        http: HttpClients,
        function_user: FunctionUser,
        function_cart,
        data_base: FacadeDB,
    ):
        """
        Удаление товара из корзины
        :param http: Клиент для запроса
        :param function_user: фикстура создающая пользователя
        :param function_cart: фикстура создающая корзину с товаром
        """
        response = http.cart_client.remove_product_from_cart(
            function_user.id,
            function_cart.product_id,
            function_user.access_token,
        )
        assert_status_code(response, HTTPStatus.OK)
        response_data = CartResponseSchema.model_validate_json(response.text)
        assert_cart_is_clear(response_data)
        assert_product_not_in_cart_db(
            function_cart.product_id, function_user.id, data_base
        )

    @pytest.mark.xfail(reason="Ожидается 404, выбрасывает 500")
    def test_delete_product_with_invalid_id(
        self,
        http: HttpClients,
        function_user: FunctionUser,
        function_cart: FunctionCart,
    ):
        response = http.cart_client.remove_product_from_cart(
            function_user.id,
            function_cart.incorrect_product_id,
            function_user.access_token,
        )
        assert_status_code(response, HTTPStatus.NOT_FOUND)

    def test_clear_cart(
        self,
        http: HttpClients,
        function_user: FunctionUser,
        function_cart: FunctionCart,
        data_base: FacadeDB,
    ):
        """
        Очистка корзины полностью
        :param http: Клиент для запроса
        :param function_user: фикстура создающая пользователя
        :param function_cart: фикстура создающая корзину с товаром
        """
        response = http.cart_client.clear_cart(
            function_user.id, function_user.access_token
        )
        assert_status_code(response, HTTPStatus.OK)
        response_data = CartResponseSchema.model_validate_json(response.text)
        assert_cart_is_clear(response_data)
        assert_cart_is_clear_db(function_user.id, data_base)

    def test_add_product_with_insufficient_stock(
        self, http: HttpClients, function_user: FunctionUser, product_over_stock_request
    ):
        """
        Добавление количества товара которого нет на складе
        :param http: Клиент для запроса
        :param function_user: фикстура создающая пользователя
        """
        request = product_over_stock_request
        response = http.cart_client.add_product_to_cart(
            function_user.id, request.model_dump(), function_user.access_token
        )
        assert_status_code(response, HTTPStatus.BAD_REQUEST)

    @pytest.mark.xfail(reason="при добавлении товара количество не обновляется")
    def test_update_cart_item_quantity(
        self,
        http: HttpClients,
        function_user: FunctionUser,
        product_to_cart: AddCartRequestSchema,
    ):
        """
        Обновление количества товара при повторном добавлении
        :param http: Клиент для запроса
        :param function_user: фикстура создающая пользователя
        :param product_to_cart: фикстура с параметрами продукта
        """
        request = product_to_cart.model_dump()
        response = None
        for product_count in range(3):
            response = http.cart_client.add_product_to_cart(
                function_user.id, request, function_user.access_token
            )

        assert_status_code(response, HTTPStatus.OK)
        response_data = CartResponseSchema.model_validate_json(response.text)
        assert_equals(response_data.items[0].quantity, 3)
