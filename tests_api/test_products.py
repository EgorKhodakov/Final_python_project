from http import HTTPStatus

import pytest

from assertions.base_assert import assert_status_code
from assertions.product_asserts import (
    all_product_field_in_response_assert,
    assert_len_product_list,
    assert_product_id,
    assert_product_price,
    assert_product_stock_quantity_is_not_null,
    product_list_fields_assert,
)
from clients.http_clients import HttpClients
from clients.products_client.product_schema import (
    ProductListSchema,
    ProductResponseSchema,
)
from db_clients.database_facade import FacadeDB


@pytest.mark.products
class TestProduct:

    def test_get_product_list(self, http: HttpClients, data_base: FacadeDB):
        """
        Получение списка продуктов
        :param http: httpx клиент для выполнения запросов
        """
        response = http.products_client.get_product_list()
        response_data = ProductListSchema.model_validate_json(response.text)
        assert_status_code(response, HTTPStatus.OK)
        assert_len_product_list(response_data, data_base)
        product_list_fields_assert(response_data)

    @pytest.mark.parametrize(
        "product_id, status_code",
        [
            ("550e8400-e29b-41d4-a716-446655440846", HTTPStatus.NOT_FOUND),
            ("", HTTPStatus.BAD_REQUEST),
        ],
    )
    def test_get_product_by_id_negative(
        self, http: HttpClients, product_id: str, status_code: int
    ):
        """
        Получение продукта по id
        :param http: httpx клиент для выполнения запросов
        :param product_id: id продукта
        :param status_code: ожидаемый в ответе статус код
        """
        response = http.products_client.get_product_by_id(product_id)
        assert_status_code(response, status_code)

    def test_get_product_by_id(self, http: HttpClients, get_product_id, data_base: FacadeDB):
        """
        Получение продукта по id
        :param http: httpx клиент для выполнения запросов
        """
        response = http.products_client.get_product_by_id(get_product_id)
        assert_status_code(response, HTTPStatus.OK)
        response_data = ProductResponseSchema.model_validate_json(response.text)
        assert_product_id(response_data, get_product_id)
        assert_product_price(response_data, response_data.product.id, data_base)
        assert_product_stock_quantity_is_not_null(response_data)
        all_product_field_in_response_assert(response_data.product)
