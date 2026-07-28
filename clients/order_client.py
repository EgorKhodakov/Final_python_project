from httpx import Response

from Schemas.order_schema import CreateOrderSchema, RefreshOrderSchema
from clients.base_client import BaseClient


class OrderClient(BaseClient):

    def create_order(self, payload: CreateOrderSchema) -> Response:
        """
        Создание заказа
        :param payload: модель создания заказа
        :return: объект httpx Response
        """
        return self._request("GET", "/v1/orders", json=payload)


    def get_orders(self, order_id) -> Response:
        """
        Получение заказа
        :param order_id: уникальный id заказа
        :return: объект httpx Response
        """
        return self._request("GET", f"/v1/orders/{order_id}")


    def cancel_order(self, order_id) -> Response:
        """
        Отмена заказа
        :param order_id: уникальный id заказа
        :return: объект httpx Response
        """
        return self._request("POST", f"/v1/orders/{order_id}/cancel")


    def refresh_order(self, order_id, payload: RefreshOrderSchema) -> Response:
        """
        Обновление статуса заказа
        :param order_id: уникальный id заказа
        :param payload: модель обновления статуса заказа
        :return: объект httpx Response
        """
        return self._request("POST", f"/v1/orders/{order_id}/status", json=payload)


