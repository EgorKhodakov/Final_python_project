import httpx
import pytest

from data.URLS import PRODUCTS_URL, BASE_URL


@pytest.fixture(scope="function")
def client():
    """
    Создание базового HTTPX клиента
    :return: возвращает httpx Client
    """
    with httpx.Client() as client:
        yield client


@pytest.fixture(scope="function")
def product_id(client):
    """
    Получение id товара
    :param client: httpx client
    :return: id товара
    """
    response = client.get(f"{PRODUCTS_URL}/prod-1")
    return response.json()["id"]


@pytest.fixture(scope="function")
def product_data(client):
    """
    Возвращает тело запроса для добавления товара в корзину
    :param client: httpx client
    :return: Тело запроса для добавления товара в корзину
    """
    return {
  "product_id": "prod-1",
  "quantity": 1
}

@pytest.fixture(scope="function")
def add_product(client, product_data):
    """
    Добавляет товар в корзину и очищает ее после теста
    :param client: httpx client
    :param product_data: Тело запроса для добавления товара в корзину
    :return:
    """
    response = client.post(f"{BASE_URL}/v1/users/user-1/cart/items", json=product_data)
    yield response
    client.delete(f"{BASE_URL}/v1/users/user-1/cart/items/{product_data['product_id']}")