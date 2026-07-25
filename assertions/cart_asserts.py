from httpx import Response

from assertions.base_asserts import assert_equals


def assert_cart_fields(actual: Response):
    """
    Проверка совпадения полей корзины
    :param actual: полученные поля
    :return:
    """
    fields = ["items", "totalPriceCents"]
    for field in fields:
        assert field in actual.json(), f"Field {field} not found in response.json"
    assert isinstance(
        actual.json()["items"], list
    ), f"Expected a list, got {type(actual.json()['items'])}"


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
