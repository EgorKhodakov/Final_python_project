from clients.user_client.user_schema import (
    CreateUserRequestShema,
    CreateUserResponseSchema,
    GetUserResponseSchema,
    LoginUserResponseSchema,
)
from fixtures.users import FunctionUser


def assert_create_user_response(
    request: CreateUserRequestShema, response: CreateUserResponseSchema
):
    """
    Проверка ответа на запрос создания пользователя
    :param request: ожидаемые параметры
    :param response: полученные параметры
    :return:
    """
    assert request.email == response.user.email
    assert request.name == response.user.name
    assert response.access_token is not None


def assert_get_user_response(request: FunctionUser, response: GetUserResponseSchema):
    """
    Проверка ответа на получение юзера
    :param request: ожидаемые параметры
    :param response: полученные параметры
    :return:
    """
    assert request.id() == response.user.id
    assert request.email() == response.user.email
    assert request.response.user.name == response.user.name
    assert request.response.user.created_at == response.user.created_at
    assert request.response.user.role == response.user.role


def assert_login_user_response(
    request: FunctionUser, response: LoginUserResponseSchema
):
    """
    Проверка ответа на запрос авторизации пользователя
    :param request: ожидаемые параметры
    :param response: полученные параметры
    :return:
    """
    assert request.id() == response.user.id
    assert request.email() == response.user.email
    assert request.name() == response.user.name
    assert request.created_at() == response.user.created_at
    assert request.role() == response.user.role
