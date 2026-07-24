import httpx
import pytest

from data.URLS import PRODUCTS_URL


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
