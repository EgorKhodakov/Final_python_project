from httpx import Response

from assertions.base_assert import assert_equals
from clients.order_client.order_schema import OrderSchema


def assert_order_status(actual: OrderSchema, expected: str):
    """
    Проверка статуса заказа
    :param expected:
    :param actual: Полученный статус
    :return:
    """
    assert_equals(actual.status, expected)


def user_id_is_correct(actual: OrderSchema, expected: str):
    """
    Проверка корректности user_id
    :param actual:
    :param expected:
    :return:
    """
    assert_equals(actual.user_id, expected)


def assert_order_id_is_correct(actual: OrderSchema, expected: str):
    """
    Проверка, что переданный id заказа соответствует полученному в ответе
    :param actual:
    :param expected:
    :return:
    """
    assert_equals(actual.id, expected)


def assert_create_order_id_is_note_none(actual: OrderSchema):
    """
    Проверка наличия id заказа в ответе на создание заказа
    :param actual:
    :return:
    """
    assert actual.id


def assert_order_price_sum_is_correct(actual: OrderSchema):
    """
    проверка совпадения стоимости товаров с общей суммой товаров
    :param actual:
    :return:
    """
    price_sum = 0
    for item in actual.items:
        price_sum += int(item.price_cents) * item.quantity
    assert_equals(price_sum, int(actual.total_amount_cents))


def assert_order_fields(actual: OrderSchema, user_id: str):
    assert_order_price_sum_is_correct(actual)
    assert_create_order_id_is_note_none(actual)
    user_id_is_correct(actual, user_id)


def assert_order_id_message(actual: Response, expected):
    """
    Проверка сообщения об ошибке создания заказа
    :param actual: Полученное сообщение
    :param expected: Ожидаемое сообщение
    :return:
    """
    actual_message = actual.json()["message"]
    assert_equals(actual_message, expected)


def assert_order_id_equals(actual: Response, expected):
    """
    Проверка соответствия order_id
    :param actual: полученный order_id
    :param expected: ожидаемый order_id
    :return:
    """
    assert_equals(actual.json()["order"]["id"], expected)
