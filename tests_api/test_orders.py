from data.URLS import BASE_URL
from assertions.base_asserts import assert_status_code, assert_body_error_code
from assertions.order_asserts import assert_order_status, assert_order_id_message
import pytest


def test_create_order(client, add_product, user_id):
    """
    Проверка создания заказа
    :param client: http client
    :param add_product: фикстура добавляющая товар в корзину
    :param user_id: фикстура возвращающая user_id
    :return:
    """
    response = client.post(f"{BASE_URL}/v1/orders", json=user_id)
    assert_status_code(response, 200)
    assert_order_status(response, "ORDER_STATUS_CREATED")


def test_create_order_without_id(client, add_product):
    """
    Проверка создания заказа без передачи id
    :param client: http client
    :param add_product: фикстура добавляющая товар в корзину
    :return:
    """
    response = client.post(f"{BASE_URL}/v1/orders", json={})
    assert_status_code(response, 400)
    assert_body_error_code(response, 3)
    assert_order_id_message(response, "user_id обязателен")

