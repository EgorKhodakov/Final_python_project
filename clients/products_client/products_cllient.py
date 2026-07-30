from httpx import Response

from clients.base_client import BaseClient


class ProductsClient(BaseClient):

    def get_product_list(self) -> Response:
        """
        Получение списка товаров
        :return: объект httpx Response
        """
        return self._request("GET", "/v1/products")

    def get_product_by_id(self, product_id: int) -> Response:
        """
        Получение товара по id
        :param product_id: уникальный id товара
        :return: объект httpx Response
        """
        return self._request("GET", f"/v1/products/{product_id}")
