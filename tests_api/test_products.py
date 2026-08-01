import pytest

from assertions.base_assert import assert_status_code
from clients.http_clients import HttpClients


def test_get_product_list(http: HttpClients):
    """
    Получение списка продуктов
    :param http: httpx клиент для выполнения запросов
    """
    response = http.products_client.get_product_list()
    assert_status_code(response, 200)


@pytest.mark.parametrize(
    "product_id, status_code",
    [
        ("550e8400-e29b-41d4-a716-446655440846", 404),
        ("550e8400-e29b-41d4-a716-446655440032", 200),
        ("", 400),
    ],
)
def test_get_product_by_id(http: HttpClients, product_id: str, status_code: int):
    """
    Получение продукта по id
    :param http: httpx клиент для выполнения запросов
    :param product_id: id продукта
    :param status_code: ожидаемый в ответе статус код
    """
    response = http.products_client.get_product_by_id(product_id)
    assert_status_code(response, status_code)
