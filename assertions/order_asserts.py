from httpx import Response

from assertions.base_assert import assert_equals


def assert_order_status(actual: Response, expected):
    """
    Проверка статуса заказа
    :param actual: Полученный статус
    :param expected: Ожидаемый статус
    :return:
    """
    actual_status = actual.json()["order"]["status"]
    assert_equals(actual_status, expected)


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
