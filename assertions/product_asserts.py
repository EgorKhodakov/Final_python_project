from requests import Response

from assertions.base_assert import assert_equals, assert_is_true
from clients.products_client.product_schema import (
    ProductListSchema,
    ProductResponseSchema,
    ProductShema,
)


def all_product_field_in_response_assert(actual: ProductShema):
    """
    Совпадения полей у конкретного продукта
    :param actual: Полученные поля
    :return:
    """
    assert_is_true(actual.id)
    assert_is_true(actual.name)
    assert_is_true(actual.description)
    assert_is_true(actual.price_cents)
    assert_is_true(actual.stock_quantity)
    assert_is_true(actual.brand)


def product_list_fields_assert(actual: ProductListSchema):
    """
    Совпадение полей у продуктов из списка
    :param actual: полученный список полей в ответе
    :return:
    """
    for product in actual.products:
        all_product_field_in_response_assert(product)


def assert_product_not_found_message(actual: Response):
    """
    Проверка сообщения при запросе отсутствующего товара
    :param actual:
    :return:
    """
    assert_equals(actual.json()["message"], "Товар с ID 'prod-25' не найден")


def assert_get_product_without_id_message(actual: Response):
    """
    Проверка сообщения при запросе товара без передачи id
    :param actual:
    :return:
    """
    assert_equals(actual.json()["message"], "ID товара не может быть пустым")


def assert_len_product_list_more_0(actual: ProductListSchema):
    """
    Сравнение длинны двух обьектов
    :param actual:
    :return:
    """
    assert len(actual.products) > 0


def assert_product_id(actual: ProductResponseSchema, expected_id: str):
    """
    Валидация полей на запрос конкретного продукта
    :param expected_id:
    :param actual:
    :return:
    """
    assert_equals(actual.product.id, expected_id)


def assert_product_price_is_not_null(actual: ProductResponseSchema):
    """
    Проверка цены товара
    :param actual:
    :return:
    """
    assert int(actual.product.price_cents) > 0


def assert_product_stock_quantity_is_not_null(actual: ProductResponseSchema):
    """
    Проверка количества товара
    :param actual:
    :return:
    """
    assert actual.product.stock_quantity > 0
