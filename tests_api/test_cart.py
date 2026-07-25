from assertions.base_asserts import assert_status_code
from assertions.cart_asserts import (asser_len_items, assert_cart_fields,
                                     assert_prise)
from data.URLS import BASE_URL


def test_get_empty_cart(client):
    """
    Получение пустой корзины
    :param client: экземпляр класса http client
    :return:
    """
    response = client.get(f"{BASE_URL}/v1/users/user-1/cart")
    assert_status_code(response, 200)


def test_card_with_product(client, add_product):
    """
    Проверка получения пустой корзины
    :param client: экземпляр класса http client
    :param add_product: фикстура добавляющая товар в корзину и очищает ее после теста
    :return:
    """
    response = add_product
    assert_status_code(response, 200)
    assert_cart_fields(response)


def test_add_product_to_cart(client, product_data):
    """
    Проверка Добавления товара в корзину
    :param client: экземпляр класса http client
    :param product_data: тело запроса для добавления продукта
    :return:
    """
    response = client.post(f"{BASE_URL}/v1/users/user-1/cart/items", json=product_data)
    assert_status_code(response, 200)
    assert_cart_fields(response)


def test_delete_product_from_cart(client, add_product):
    """
    Проверка удаления товара из корзины
    :param client: экземпляр класса http client
    :param add_product: фикстура добавляющая товар в корзину и очищает ее после теста
    :return:
    """
    product_in_cart = add_product
    assert_status_code(product_in_cart, 200)
    prod_id = product_in_cart.json()["items"][0]["productId"]
    response = client.delete(f"{BASE_URL}/v1/users/user-1/cart/items/{prod_id}")
    assert_status_code(response, 200)


def test_clear_cart(client, add_product):
    """
    Проверка очистки корзины
    :param client: экземпляр класса http client
    :param add_product: фикстура добавляющая товар в корзину и очищает ее после теста
    :return:
    """
    response = client.delete(f"{BASE_URL}/v1/users/user-1/cart")
    assert_status_code(response, 200)
    assert_prise(response, "0")
    asser_len_items(response, 0)
