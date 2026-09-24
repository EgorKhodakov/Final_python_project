from httpx import Response

from clients.base_client import BaseClient
from clients.cart_client.cart_schema import AddCartRequestSchema, PromocodeSchema


class CartClient(BaseClient):

    def get_cart(self, user_id: str, access_token: str) -> Response:
        """
        Получение корзины
        :param access_token: токен авторизации
        :param user_id: уникальный id пользователя
        :return: объект httpx Response
        """
        return self._request(
            "GET", f"/v1/users/{user_id}/cart", access_token=access_token
        )

    def add_product_to_cart(
        self, user_id: str, request: AddCartRequestSchema, access_token: str
    ) -> Response:
        """
        Добавление продукта в корзину
        :param access_token:
        :param request:
        :param user_id: уникальный id пользователя
        :return: объект httpx Response
        """
        return self._request(
            "POST",
            f"/v1/users/{user_id}/cart/items",
            json=request,
            access_token=access_token,
        )

    def remove_product_from_cart(
        self, user_id: str, product_id: str, access_token: str
    ) -> Response:
        """
        Удаление продукта из корзины
        :param access_token:
        :param user_id: уникальный id пользователя
        :param product_id: Уникальный id продукта
        :return: объект httpx Response
        """
        return self._request(
            "DELETE",
            f"/v1/users/{user_id}/cart/items/{product_id}",
            access_token=access_token,
        )

    def clear_cart(self, user_id: str, access_token: str) -> Response:
        """
        Очищение корзины
        :param access_token:
        :param user_id: уникальный id пользователя
        :return: объект httpx Response
        """
        return self._request(
            "DELETE", f"/v1/users/{user_id}/cart", access_token=access_token
        )

    def add_promocode_to_cart(
        self, user_id: str, paylod: PromocodeSchema, access_token: str
    ) -> Response:
        """
        Добавление промокода в корзину
        :param access_token:
        :param user_id: уникальный id пользователя
        :param paylod: модель тела запроса промокода
        :return: объект httpx Response
        """
        return self._request(
            "POST",
            f"/v1/users/{user_id}/cart/promocode",
            json=paylod.model_dump(),
            access_token=access_token,
        )

    def remove_promocode_from_cart(self, user_id: str, access_token: str) -> Response:
        """
        Удаление промокода из корзины
        :param user_id: уникальный id пользователя
        :return: объект httpx Response
        """
        return self._request(
            "DELETE", f"/v1/users/{user_id}/cart/promocode", access_token=access_token
        )
