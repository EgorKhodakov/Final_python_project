import httpx
import pytest

from data.URLS import BASE_URL, PRODUCTS_URL


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
    return {"product_id": "prod-1", "quantity": 1}


@pytest.fixture(scope="function")
def add_product(client, product_data):
    """
    Добавляет товар в корзину и очищает ее после теста
    :param client: httpx client
    :param product_data: Тело запроса для добавления товара в корзину
    :return: корзина с товаром
    """
    response = client.post(f"{BASE_URL}/v1/users/user-1/cart/items", json=product_data)
    yield response
    client.delete(f"{BASE_URL}/v1/users/user-1/cart/items/{product_data['product_id']}")


@pytest.fixture(scope="function")
def user_id():
    """
    Возвращает user_id
    :return: user_id
    """
    return {"user_id": "user-1"}


@pytest.fixture(scope="function")
def create_order(client, add_product, user_id):
    """
    Фикстура для создания заказа
    :param client:
    :param add_product: фикстура добавляющая товар в корзину
    :param user_id: фикстура возвращающая user_id
    :return: response объект заказа
    """
    response = client.post(f"{BASE_URL}/v1/orders", json=user_id)
    return response


@pytest.fixture(scope="function")
def order_id(create_order):
    """
    Фикстура для возврата order_id
    :param create_order: фиктура для создания заказа
    :return: user_id
    """
    order_id = create_order.json()["order"]["id"]
    return order_id
