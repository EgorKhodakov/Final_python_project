from httpx import Response

from clients.base_client import BaseClient
from schemas.cart_schema import CartSchema, PromocodeSchema


class CartClient(BaseClient):

    def get_cart(self, user_id: str) -> Response:
        """
        Получение корзины
        :param user_id: уникальный id пользователя
        :return: объект httpx Response
        """
        return self._request("GET", f"/v1/users/{user_id}/cart")

    def add_product_to_cart(self, user_id: str, payload: CartSchema) -> Response:
        """
        Добавление продукта в корзину
        :param user_id: уникальный id пользователя
        :param payload: Модель ответа на получение корзины
        :return: объект httpx Response
        """
        return self._request(
            "POST", f"/v1/users/{user_id}/cart/items", json=payload.model_dump()
        )

    def remove_product_from_cart(self, user_id: str, product_id: str) -> Response:
        """
        Удаление продукта из корзины
        :param user_id: уникальный id пользователя
        :param product_id: Уникальный id продукта
        :return: объект httpx Response
        """
        return self._request("DELETE", f"/v1/users/{user_id}/cart/items/{product_id}")

    def clear_cart(self, user_id: str) -> Response:
        """
        Очищение корзины
        :param user_id: уникальный id пользователя
        :return: объект httpx Response
        """
        return self._request("DELETE", f"/v1/users/{user_id}/cart")

    def add_promocode_to_cart(self, user_id: str, paylod: PromocodeSchema) -> Response:
        """
        Добавление промокода в корзину
        :param user_id: уникальный id пользователя
        :param paylod: модель тела запроса промокода
        :return: объект httpx Response
        """
        return self._request(
            "POST", f"/v1/users/{user_id}/cart/promocode", json=paylod.model_dump()
        )

    def remove_promocode_from_cart(self, user_id: str) -> Response:
        """
        Удаление промокода из корзины
        :param user_id: уникальный id пользователя
        :return: объект httpx Response
        """
        return self._request("DELETE", f"/v1/users/{user_id}/cart/promocode")
