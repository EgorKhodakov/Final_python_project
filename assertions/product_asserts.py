from requests import Response

from assertions.base_assert import assert_equals, assert_is_true, assert_len
from clients.products_client.product_schema import (
    ProductListSchema,
    ProductResponseSchema,
    ProductShema,
)
from db_clients.database_facade import FacadeDB


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


def assert_len_product_list(actual: ProductListSchema, data_base: FacadeDB):
    """
    Сравнение длинны двух обьектов
    :param data_base:
    :param actual:
    :return:
    """
    len_product_list = data_base.products.get_product_list_count()
    assert_len(actual.products, len_product_list)


def assert_product_id(actual: ProductResponseSchema, expected_id: str):
    """
    Валидация полей на запрос конкретного продукта
    :param expected_id:
    :param actual:
    :return:
    """
    assert_equals(actual.product.id, expected_id)


def assert_product_price(actual: ProductResponseSchema, product_id: str , data_base: FacadeDB):
    """
    Проверка цены товара
    :param product_id:
    :param data_base:
    :param actual:
    :return:
    """
    price = data_base.products.get_product_price(product_id)
    assert_equals(int(actual.product.price_cents), price)


def assert_product_stock_quantity_is_not_null(actual: ProductResponseSchema):
    """
    Проверка количества товара
    :param actual:
    :return:
    """
    assert actual.product.stock_quantity > 0
