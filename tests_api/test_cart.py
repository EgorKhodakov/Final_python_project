import pytest

from assertions.base_assert import assert_status_code
from assertions.cart_asserts import assert_cart_fields
from clients.http_clients import HttpClients
from fixtures.cart import FunctionCart
from fixtures.users import FunctionUser


def test_get_cart(http: HttpClients, function_user: FunctionUser):
    response = http.cart_client.get_cart(
        function_user.id(), function_user.access_token()
    )
    assert_status_code(response, 200)



def test_add_product_to_cart(http: HttpClients, function_user: FunctionUser):
    request = {"product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 1}
    response = http.cart_client.add_product_to_cart(
        function_user.id(), request, function_user.access_token()
    )
    assert_status_code(response, 200)
    assert_cart_fields(response)


def test_delete_product_from_cart(
    http: HttpClients, function_user: FunctionUser, function_cart
):
    response = http.cart_client.remove_product_from_cart(
        function_user.id(), function_cart.product_id(), function_user.access_token()
    )
    assert_status_code(response, 200)


def test_delete_none_product_from_cart(
    http: HttpClients, function_user: FunctionUser, function_cart: FunctionCart
):
    response = http.cart_client.remove_product_from_cart(
        function_user.id(),
        "550e8400-e29b-41d4-a716-446655440008",
        function_user.access_token(),
    )
    assert_status_code(response, 500)


def test_clear_cart(
    http: HttpClients, function_user: FunctionUser, function_cart: FunctionCart
):
    response = http.cart_client.clear_cart(
        function_user.id(), function_user.access_token()
    )
    assert_status_code(response, 200)


def test_add_product_with_insufficient_stock(
    http: HttpClients, function_user: FunctionUser
):
    request = {"product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 99999}
    response = http.cart_client.add_product_to_cart(
        function_user.id(), request, function_user.access_token()
    )
    assert_status_code(response, 400)


@pytest.mark.xfail
def test_update_cart_item_quantity(http: HttpClients, function_user: FunctionUser):
    request = {"product_id": "550e8400-e29b-41d4-a716-446655440001", "quantity": 1}
    for i in range(1, 3):
        response = http.cart_client.add_product_to_cart(
            function_user.id(), request, function_user.access_token()
        )
        assert_status_code(response, 200)
        assert response.json()["items"][0]["quantity"] == i
