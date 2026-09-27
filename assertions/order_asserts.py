from httpx import Response

from assertions.base_assert import assert_equals, assert_is_true, assert_len
from clients.order_client.order_schema import OrderSchema, CreateOrderResponseSchema
from db_clients.database_facade import FacadeDB


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


def assert_order_in_db(actual_order_id: CreateOrderResponseSchema, user_id, data_base: FacadeDB):
    """
    Проверка соответствия номера заказа
    :param actual_order_id: полученный id заказа
    :param user_id: id пользователя
    :param data_base: фикстура для запросов к БД
    """
    expected_order = data_base.orders.get_order_id(user_id)
    assert_equals(actual_order_id.order.id, expected_order[0])


def assert_order_status_in_db(actual_status: int, user_id, data_base: FacadeDB):
    db_order_status = data_base.orders.get_order_status(user_id)
    assert_equals(actual_status, db_order_status)


def assert_order_sum_in_bd(actual: CreateOrderResponseSchema, user_id, data_base: FacadeDB):
    order_sum = data_base.orders.get_total_amount_cents(user_id)[0][0]
    assert_equals(int(actual.order.total_amount_cents), order_sum)


