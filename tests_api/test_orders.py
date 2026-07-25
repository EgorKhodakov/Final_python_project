import pytest

from assertions.base_asserts import (assert_body_error_code,
                                     assert_response_error_message,
                                     assert_status_code)
from assertions.order_asserts import (assert_order_id_equals,
                                      assert_order_id_message,
                                      assert_order_status)
from data.URLS import BASE_URL


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


def test_get_order_by_id(client, order_id):
    """
    Проверка получения заказа по id
    :param client: http client
    :param order_id: фикстура создающая заказ и возвращающая order_id
    :return:
    """
    response = client.get(f"{BASE_URL}/v1/orders/{order_id}")
    assert_status_code(response, 200)
    assert_order_id_equals(response, order_id)


@pytest.mark.parametrize(
    "order_id, response_code, message, error_code",
    [("", 400, "order_id обязателен", 3), ("ord-12344321", 404, "заказ не найден", 5)],
)
def test_get_order_by_incorrect_id(
    client, create_order, order_id, response_code, message, error_code
):
    """
    Проверка запроса заказа при некорректном id
    :param client:
    :param create_order: фикстура создающая заказ
    :param order_id: id заказа
    :param response_code: ожидаемый код ответа
    :param message: ожидаемое сообщение в теле ответа
    :param error_code: код ошибки в теле ответа
    :return:
    """
    response = client.get(f"{BASE_URL}/v1/orders/{order_id}")
    assert_status_code(response, response_code)
    assert_body_error_code(response, error_code)
    assert_response_error_message(response, message)
