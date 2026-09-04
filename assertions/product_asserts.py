from requests import Response

from assertions.base_assert import assert_equals
from clients.products_client.product_schema import (
    ProductListSchema,
    ProductShema,
    ProductResponseSchema,
)


def fields_assert(actual):
    """
    Совпадения полей у конкретного продукта
    :param actual: Полученные поля
    :return:
    """
    fields = ["id", "name", "description", "priceCents", "stockQuantity"]
    for field in fields:
        assert field in actual


def product_list_fields_assert(actual):
    """
    Совпадение полей у продуктов из списка
    :param actual: полученный список полей в ответе
    :return:
    """
    for field in actual.json()["products"]:
        fields_assert(field)


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


def assert_product_list_fields(actual):
    """
    Валидация полей ответа на запрос списка продуктов
    :param actual:
    :return:
    """
    assert ProductListSchema.model_validate_json(actual.text)


def assert_product_id(actual: ProductResponseSchema, expected_id: str):
    """
    Валидация полей на запрос конкретного продукта
    :param actual:
    :return:
    """
    assert_equals(actual.product.id, expected_id)


def assert_product_price(actual: ProductResponseSchema):
    """
    Проверка цены товара
    :param actual:
    :return:
    """
    assert actual.product.stock_quantity > 0


def assert_product_stock_quantity(actual: ProductResponseSchema):
    """
    Проверка количества товара
    :param actual:
    :return:
    """
    assert actual.product.stock_quantity > 0
