from httpx import Response

from clients.base_client import BaseClient
from data.urls import LOGIN_URL, REGISTATION_URL
from Schemas.login_schema import LoginUserSchema
from Schemas.user_schema import CreateUserShema


class AuthClient(BaseClient):

    def registration_user(self, creds: CreateUserShema) -> Response:
        """
        Регистрация пользователя
        :param creds: модель для регистрации пользователя
        :return: экземпляр класса httpx Response
        """
        return self._request("POST", f"{REGISTATION_URL}", json=creds.model_dump())

    def login_user(self, creds: LoginUserSchema) -> Response:
        """
        Авторизация пользователя
        :param creds: Модель для авторизации пользователя
        :return: экземпляр класса httpx Response
        """
        return self._request("POST", f"{LOGIN_URL}", json=creds.model_dump())

    def get_user_by_id(self, user_id: int) -> Response:
        """
        Получение пользователя по id
        :param user_id: уникальный id пользователя
        :return: экземпляр класса httpx Response
        """
        return self._request("GET", f"/v1/users/{user_id}")
