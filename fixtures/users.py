from typing import Any, Generator

import pytest
from pydantic import BaseModel

from clients.user_client.user_schema import (
    CreateUserRequestShema,
    CreateUserResponseSchema, LoginUserRequestSchema,
)




class FunctionUser(BaseModel):
    """
    Класс для агрегации возвращаемых фикстурой function_user данных
    """

    request: CreateUserRequestShema
    response: CreateUserResponseSchema

    @property
    def id(self) -> str:
        """
        Возвращает id пользователя
        :return:
        """
        return self.response.user.id

    @property
    def incorrect_id(self):
        """
        Возвращает не корректный id пользователя
        :return:
        """
        return self.response.user.id[:-3] + "asd"

    @property
    def password(self) -> str:
        """
        Возвращает пароль пользователя
        :return:
        """
        return self.request.password

    @property
    def email(self) -> str:
        """
        Возвращает email пользователя
        :return:
        """
        return self.request.email

    @property
    def access_token(self) -> str:
        """
        Возвращает авторизационный токен
        :return:
        """
        return self.response.access_token

    @property
    def name(self) -> str:
        """
        Возвращает имя пользователя
        :return:
        """
        return self.response.user.name

    @property
    def created_at(self):
        """
        Возвращает время создания пользователя
        :return:
        """
        return self.response.user.created_at

    @property
    def role(self) -> str:
        """
        Возвращает роль пользователя
        :return:
        """
        return self.response.user.role

    @property
    def valid_login_payload(self):
        return LoginUserRequestSchema(
            email=self.email,
            password=self.password,
        )

    @property
    def login_payload_with_invalid_password(self):
        return LoginUserRequestSchema(
            email=self.email,
            password=self.password[:-4]+"aaws",
        )


@pytest.fixture(scope="function")
def function_user(http) -> Generator[FunctionUser, Any, None]:
    """
    Фикстура возвращающая готового юзера
    :param http:
    :return:
    """
    request = CreateUserRequestShema()
    response = http.auth_client.create_user(request)
    user = FunctionUser(request=request, response=response)
    yield user
    http.auth_client.delete_user_api(user.id, access_token=response.access_token)
