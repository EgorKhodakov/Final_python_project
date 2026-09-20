from pydantic import UUID4

from assertions.base_assert import assert_equals, assert_is_true, assert_len
from clients.user_client.user_schema import (
    BaseUserSchema,
    CreateUserRequestShema,
    CreateUserResponseSchema,
    GetUserResponseSchema,
    LoginUserResponseSchema,
)
from db_clients.database_facade import FacadeDB
from fixtures.users import FunctionUser


def assert_user_fields_equal(request: FunctionUser, response_user: BaseUserSchema):
    """
    Базовая проверка поле ответа юзера
    :param request: FunctionUser с ожидаемыми данными
    :param response_user: объект user из ответа
    :return:
    """

    assert_equals(request.id, response_user.id)
    assert_equals(request.email, response_user.email)
    assert_equals(request.name, response_user.name)
    assert_equals(request.created_at, response_user.created_at)
    assert_equals(request.role, response_user.role)


def assert_create_user_response(
    request: CreateUserRequestShema, response: CreateUserResponseSchema
):
    """
    Проверка ответа на запрос создания пользователя
    :param request: ожидаемые параметры
    :param response: полученные параметры
    :return:
    """
    UUID4(response.user.id)  # Проверка, что формат id корректный
    assert_equals(request.email, response.user.email)
    assert_equals(request.name, response.user.name)
    assert_is_true(response.user.created_at)
    assert_equals(response.user.role, "user")
    parts = response.access_token.split(
        "."
    )  # Проверка, что токен состоит из трех частей
    assert_len(parts, 3)
    assert_is_true(all(parts))


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


def assert_user_id_in_db(user_id: str, data_base: FacadeDB):
    """
    Проверка, что созданный пользователь присутствует в базе данных
    :param user_id: id пользователя
    :param data_base: фикстура для запросов к БД
    """
    user = data_base.users.get_user_by_id(user_id)
    assert_len(user, 1)
    assert_equals(user[0][0], user_id)


def assert_email_in_db(api_email: str, user_id: str, data_base: FacadeDB):
    """
    :param api_email: email переданный в запросе на регистрацию пользователя
    :param user_id: id для получения email юзера
    :param data_base: фикстура для запросов к БД
    """
    db_email = data_base.users.get_user_email(user_id)[0][0]
    assert_equals(api_email, db_email)

