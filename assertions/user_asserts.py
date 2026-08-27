from clients.user_client.user_schema import (
    CreateUserRequestShema,
    CreateUserResponseSchema,
    GetUserResponseSchema,
    LoginUserResponseSchema, BaseUserSchema,
)
from fixtures.users import FunctionUser
from pydantic import UUID4


def assert_user_fields_equal(request: FunctionUser, response_user: BaseUserSchema):
    """
    Базовая проверка поле ответа юзера
    :param request: FunctionUser с ожидаемыми данными
    :param response_user: объект user из ответа
    :return:
    """
    assert request.id() == response_user.id
    assert request.email() == response_user.email
    assert request.name() == response_user.name
    assert request.created_at() == response_user.created_at
    assert request.role() == response_user.role

def assert_create_user_response(
    request: CreateUserRequestShema, response: CreateUserResponseSchema
):
    """
    Проверка ответа на запрос создания пользователя
    :param request: ожидаемые параметры
    :param response: полученные параметры
    :return:
    """
    UUID4(response.user.id)
    assert request.email == response.user.email
    assert request.name == response.user.name

    parts = response.access_token.split(".")
    assert len(parts) == 3
    assert all(parts)


def assert_get_user_response(request: FunctionUser, response: GetUserResponseSchema):
    """
    Проверка ответа на получение юзера
    :param request: ожидаемые параметры
    :param response: полученные параметры
    :return:
    """
    assert_user_fields_equal(request, response.user)


def assert_login_user_response(
    request: FunctionUser, response: LoginUserResponseSchema
):
    """
    Проверка ответа на запрос авторизации пользователя
    :param request: ожидаемые параметры
    :param response: полученные параметры
    :return:
    """
    assert_user_fields_equal(request, response.user)