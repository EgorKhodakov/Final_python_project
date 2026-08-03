import pytest
from pydantic import BaseModel

from clients.user_client.user_schema import (CreateUserResponseSchema,
                                             CreateUserRequestShema)


class FunctionUser(BaseModel):
    """
    Класс для агрегации возвращаемых фикстурой function_user данных
    """
    request: CreateUserRequestShema
    response: CreateUserResponseSchema

    def id(self) -> str:
        """
        Возвращает id пользователя
        :return:
        """
        return self.response.user.id

    def password(self) -> str:
        """
        Возвращает пароль пользователя
        :return:
        """
        return self.request.password

    def email(self) -> str:
        """
        Возвращает email пользователя
        :return:
        """
        return self.request.email

    def access_token(self) -> str:
        """
        Возвращает авторизационный токен
        :return:
        """
        return self.response.accessToken

    def name(self) -> str:
        """
        Возвращает имя пользователя
        :return:
        """
        return self.response.user.name

    def createdAt(self):
        """
        Возвращает время создания пользователя
        :return:
        """
        return self.response.user.createdAt

    def role(self) -> str:
        """
        Возвращает роль пользователя
        :return:
        """
        return self.response.user.role


@pytest.fixture(scope="function")
def function_user(http) -> FunctionUser:
    """
    Фикстура возвращающая готового юзера
    :param http:
    :return:
    """
    request = CreateUserRequestShema()
    response = http.auth_client.create_user(request)
    return FunctionUser(request=request, response=response)
