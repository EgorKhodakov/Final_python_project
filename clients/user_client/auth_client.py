from httpx import Response

from clients.user_client.login_schema import LoginUserSchema
from clients.user_client.user_schema import (CreateUserResponseSchema,
                                             CreateUserShema)
from clients.base_client import BaseClient
from data.urls import LOGIN_URL, REGISTATION_URL


class AuthClient(BaseClient):

    def create_user_api(self, creds: CreateUserShema) -> Response:
        """
        Регистрация пользователя
        :param creds: модель для регистрации пользователя
        :return: экземпляр класса httpx Response
        """
        return self._request("POST", f"{REGISTATION_URL}", json=creds.model_dump())

    def login_user_api(self, creds: LoginUserSchema) -> Response:
        """
        Авторизация пользователя
        :param creds: Модель для авторизации пользователя
        :return: экземпляр класса httpx Response
        """
        return self._request("POST", f"{LOGIN_URL}", json=creds.model_dump())

    def get_user_by_id_api(self, user_id: int) -> Response:
        """
        Получение пользователя по id
        :param user_id: уникальный id пользователя
        :return: экземпляр класса httpx Response
        """
        return self._request("GET", f"/v1/users/{user_id}")

    def create_user(self, request: CreateUserShema) -> CreateUserResponseSchema:
        response = self.create_user_api(request)
        return CreateUserResponseSchema.model_validate_json(response.text)
