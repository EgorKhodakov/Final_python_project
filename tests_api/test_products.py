import pytest

from assertions.base_asserts import assert_body_error_code, assert_status_code
from assertions.product_assertions import (
    assert_get_product_without_id_message, assert_product_not_found_message,
    fields_assert, product_list_fields_assert)
from data.URLS import PRODUCTS_URL


@pytest.mark.parametrize("product", ["prod-1", "prod-2"])
def test_get_product_by_id(client, product):
    """
    Получение товара по ID
    :param client: Базовый httpx client для запросов
    :return:
    """
    response = client.get(f"{PRODUCTS_URL}/{product}")
    assert_status_code(response, 200)
    body = response.json()
    fields_assert(body["product"])


def test_product_by_id_not_found(client):
    """
    Запрос товара с несуществующим id
    :param client: Базовый httpx client для запросов
    :return:
    """
    response = client.get(f"{PRODUCTS_URL}/prod-25")
    assert_status_code(response, 404)
    assert_body_error_code(response, 5)
    assert_product_not_found_message(response)


def test_get_product_without_id(client):
    """
    Получение товара без id в запросе
    :param client: Базовый httpx client для запросов
    :return:
    """
    response = client.get(f"{PRODUCTS_URL}/")
    assert_status_code(response, 400)
    assert_body_error_code(response, 3)
    assert_get_product_without_id_message(response)


def test_get_all_products(client):
    """
    Получение всего списка товаров
    :param client: Базовый httpx client для запросов
    :return:
    """
    response = client.get(f"{PRODUCTS_URL}")
    assert_status_code(response, 200)
    product_list_fields_assert(response)
