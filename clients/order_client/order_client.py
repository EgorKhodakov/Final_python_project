from wsgiref import headers

from httpx import Response

from clients.base_client import BaseClient
from clients.order_client.order_schema import CreateOrderSchema, RefreshOrderSchema


class OrderClient(BaseClient):

    def create_order(self, request: CreateOrderSchema, access_token: str) -> Response:
        """
        Создание заказа
        :param access_token: токен авторизации
        :param request: модель создания заказа
        :return: объект httpx Response
        """
        return self._request(
            "POST", "/v1/orders", json=request.model_dump(), access_token=access_token
        )

    def get_order(self, order_id, access_token: str) -> Response:
        """
        Получение заказа
        :param access_token: токен авторизации
        :param order_id: уникальный id заказа
        :return: объект httpx Response
        """
        return self._request("GET", f"/v1/orders/{order_id}", access_token=access_token)

    def get_orders(self, user_id, access_token: str) -> Response:
        """
        Получение заказа
        :param access_token: токен авторизации
        :param user_id: уникальный id юзера
        :return: объект httpx Response
        """
        return self._request(
            "GET", f"/v1/users/{user_id}/orders", access_token=access_token
        )

    def cancel_order(self, order_id, access_token: str) -> Response:
        """
        Отмена заказа
        :param access_token: токен авторизации
        :param order_id: уникальный id заказа
        :return: объект httpx Response
        """
        return self._request(
            "POST", f"/v1/orders/{order_id}/cancel", access_token=access_token
        )

    def refresh_order(
        self, order_id, payload: RefreshOrderSchema, access_token: str
    ) -> Response:
        """
        Обновление статуса заказа
        :param access_token: токен авторизации
        :param order_id: уникальный id заказа
        :param payload: модель обновления статуса заказа
        :return: объект httpx Response
        """
        return self._request(
            "POST",
            f"/v1/orders/{order_id}/status",
            json=payload.model_dump(),
            access_token=access_token,
        )

    def delete_order(self, order_id, access_token: str) -> Response:
        """
        Удаление заказа
        :param order_id: id заказа
        :param access_token: токен авторизации
        :return:
        """
        return self._request(
            "DELETE", f"/v1/orders/{order_id}", access_token=access_token
        )
