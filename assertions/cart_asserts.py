from httpx import Response

from assertions.base_assert import assert_equals, assert_is_true, assert_len
from clients.cart_client.cart_schema import AddCartRequestSchema, CartResponseSchema


def assert_cart_fields(actual: Response):
    """
    Валидация полей и типов данных корзины
    :param actual: полученные поля
    """
    CartResponseSchema.model_validate_json(actual.text)


def assert_add_product_id_and_quantity(
    actual: CartResponseSchema, expected: AddCartRequestSchema
):
    """
    Проверка, что добавленный в корзину товар совпадает по id и количеству с переданным товаром
    :param actual: Полученный ответ от апи
    :param expected: Ожидаемый ответ
    """
    assert_equals(actual.items[0].product_id, expected.product_id)
    assert_equals(actual.items[0].quantity, expected.quantity)


def assert_price(
    actual: CartResponseSchema, expected_price
):  # для проверки нужно подключить БД
    """
    Проверка совпадения цены товара
    :param actual: полученная цена
    :param expected_price: ожидаемая цена
    """
    assert_equals(actual.total_price_cents, expected_price)


def asser_len_items(actual: CartResponseSchema, expected_len):
    """
    Проверка длинны списка товаров в корзине
    :param actual: полученная длинна корзины
    :param expected_len: ожидаемая длинна корзины
    """
    assert_len((actual.items), expected_len)


def assert_cart_is_clear(actual: CartResponseSchema):
    """
    Проверка, что корзина очистилась
    :param actual:
    """
    assert_is_true(not actual.items)
    assert_equals(actual.total_price_cents, "0")
