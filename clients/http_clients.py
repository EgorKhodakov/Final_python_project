from httpx import Client
from clients.auth_client.auth_client import AuthClient
from clients.cart_client.cart_client import CartClient
from clients.order_client.order_client import OrderClient
from clients.products_client.products_cllient import ProductsClient


class HttpClients:
    def __init__(self, http_client: Client):
        self.auth_client = AuthClient(http_client)
        self.cart_client = CartClient(http_client)
        self.order_client = OrderClient(http_client)
        self.products_client = ProductsClient(http_client)