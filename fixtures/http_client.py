import httpx
import pytest

from clients.http_clients import HttpClients
from data.urls import BASE_URL


@pytest.fixture(scope="session")
def http():
    with httpx.Client(base_url=BASE_URL) as client:
        api_facade = HttpClients(client)
        yield api_facade
