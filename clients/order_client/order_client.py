from httpx import Response

from clients.base_client import BaseClient
from clients.order_client.order_schema import CreateOrderSchema, RefreshOrderSchema


class OrderClient(BaseClient):

    def create_order(self, request: CreateOrderSchema, access_token: str) -> Response:
        """
        Создание заказа
        :param request: модель создания заказа
        :return: объект httpx Response
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        return self._request(
            "POST", "/v1/orders", json=request.model_dump(), headers=headers
        )

    def get_orders(self, order_id, access_token: str) -> Response:
        """
        Получение заказа
        :param order_id: уникальный id заказа
        :return: объект httpx Response
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        return self._request("GET", f"/v1/orders/{order_id}", headers=headers)

    def cancel_order(self, order_id, access_token: str) -> Response:
        """
        Отмена заказа
        :param order_id: уникальный id заказа
        :return: объект httpx Response
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        return self._request("POST", f"/v1/orders/{order_id}/cancel", headers=headers)

    def refresh_order(
        self, order_id, payload: RefreshOrderSchema, access_token: str
    ) -> Response:
        """
        Обновление статуса заказа
        :param order_id: уникальный id заказа
        :param payload: модель обновления статуса заказа
        :return: объект httpx Response
        """
        headers = {"Authorization": f"Bearer {access_token}"}
        return self._request(
            "POST",
            f"/v1/orders/{order_id}/status",
            json=payload.model_dump(),
            headers=headers,
        )
