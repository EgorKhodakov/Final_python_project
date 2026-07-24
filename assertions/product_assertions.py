from requests import Response

from assertions.base_asserts import assert_equals


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
