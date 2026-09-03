from httpx import Response

from assertions.base_assert import assert_equals
from clients.cart_client.cart_schema import CartResponseSchema, AddCartRequestSchema


def assert_cart_fields(actual: CartResponseSchema):
    """
    Валидация полей и типов данных корзины
    :param actual: полученные поля
    :return:
    """
    CartResponseSchema.model_validate_json(actual.text)


def assert_add_product_id_and_quantity(
    actual: CartResponseSchema, expected: AddCartRequestSchema
):
    """
    Проверка, что добавленный в корзину товар совпадает по id и количеству с переданным товаром
    :param actual: Полученный ответ от апи
    :param expected: Ожидаемый ответ
    :return:
    """
    assert_equals(actual.items[0].product_id, expected.product_id)
    assert_equals(actual.items[0].quantity, expected.quantity)


def assert_prise(actual: Response, expected_price):
    """
    Проверка совпадения цены товара
    :param actual: полученная цена
    :param expected_price: ожидаемая цена
    :return:
    """
    assert_equals(actual.json()["totalPriceCents"], expected_price)


def asser_len_items(actual: Response, expected_len):
    """
    Проверка длинны списка товаров в корзине
    :param actual: полученная длинна корзины
    :param expected_len: ожидаемая длинна корзины
    :return:
    """
    assert_equals(len(actual.json()["items"]), expected_len)
