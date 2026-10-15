import pytest


@pytest.fixture(scope="function")
def get_product_id():
    return "550e8400-e29b-41d4-a716-446655440032"
