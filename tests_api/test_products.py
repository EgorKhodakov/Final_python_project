import pytest

from assertions.base_assert import assert_status_code
from assertions.product_asserts import (
    assert_len_product_list_more_0,
    assert_product_list_fields,
    assert_product_stock_quantity,
    assert_product_id,
    assert_product_price,
)
from clients.http_clients import HttpClients
from clients.products_client.product_schema import (
    ProductListSchema,
    ProductShema,
    ProductResponseSchema,
)


def test_get_product_list(http: HttpClients):
    """
    Получение списка продуктов
    :param http: httpx клиент для выполнения запросов
    """
    response = http.products_client.get_product_list()
    response_data = ProductListSchema.model_validate_json(response.text)
    assert_status_code(response, 200)
    assert_len_product_list_more_0(response_data)
    assert_product_list_fields(response)


@pytest.mark.parametrize(
    "product_id, status_code",
    [
        ("550e8400-e29b-41d4-a716-446655440846", 404),
        ("", 400),
    ],
)
def test_get_product_by_id_negative(
    http: HttpClients, product_id: str, status_code: int
):
    """
    Получение продукта по id
    :param http: httpx клиент для выполнения запросов
    :param product_id: id продукта
    :param status_code: ожидаемый в ответе статус код
    """
    response = http.products_client.get_product_by_id(product_id)
    assert_status_code(response, status_code)


def test_get_product_by_id(http: HttpClients):
    """
    Получение продукта по id
    :param http: httpx клиент для выполнения запросов
    """
    product_id = "550e8400-e29b-41d4-a716-446655440032"
    response = http.products_client.get_product_by_id(product_id)
    assert_status_code(response, 200)
    response_data = ProductResponseSchema.model_validate_json(response.text)
    assert_product_id(response_data, product_id)
    assert_product_price(response_data)
    assert_product_stock_quantity(response_data)
