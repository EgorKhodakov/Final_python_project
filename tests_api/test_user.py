import pytest

from assertions.base_assert import assert_status_code
from assertions.user_asserts import (
    assert_create_user_response,
    assert_get_user_response, assert_login_user_response,
)
from clients.http_clients import HttpClients
from clients.user_client.user_schema import (
    CreateUserRequestShema,
    CreateUserResponseSchema,
    GetUserResponseSchema,
    LoginUserRequestSchema, LoginUserResponseSchema,
)
from fixtures.users import FunctionUser
from tools.fakers import fake


def test_create_user(http: HttpClients):
    """
    Создание пользователя
    :param http:
    :return:
    """
    request = CreateUserRequestShema()
    response = http.auth_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)
    assert_status_code(response, 200)
    assert_create_user_response(request, response_data)


def test_get_user_by_id(http: HttpClients, function_user: FunctionUser):
    """
    Получение пользователя по id
    :param http:
    :param function_user:
    :return:
    """
    user_id = function_user.id()
    response = http.auth_client.get_user_by_id_api(user_id)
    response_data = GetUserResponseSchema.model_validate_json(response.text)
    assert_status_code(response, 200)
    assert_get_user_response(function_user, response_data)


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("", "", 400),
        ("validemail@google.com", "", 400),
        ("", "validpassq34%$^", 400),
        ("invalid-email", "validpassq34%$^", 401),
        ("nonexistent@yahoo.ru", "validpassq34%$^", 401),
    ],
    ids=[
        "login_without_email_and_password",
        "login_without_password",
        "login_without_email",
        "login_with_invalid_email",
        "login_with_nonexistent_email",
    ],
)
def test_login_user_negative(http: HttpClients, email, password, status_code):
    """
    Авторизация пользователя
    :param http:
    :return:
    """

    request = LoginUserRequestSchema(email=email, password=password)
    response = http.auth_client.login_user_api(request)

    assert_status_code(response, status_code)


@pytest.mark.parametrize(
    "user_id, status_code",
    [
        (fake.uid(), 404),
        pytest.param(
            "sdafwer423434334fv",
            400,
            marks=pytest.mark.xfail(
                reason="некорректный запрос, ожидается 400, приходит 500"
            ),
        ),
        pytest.param(
            None,
            400,
            marks=pytest.mark.xfail(
                reason="некорректный запрос, ожидается 400, приходит 500"
            ),
        ),
    ],
    ids=[
        "get_user_with_non_existent_id",
        "get_user_by_incorrect_id",
        "get_user_without_id",
    ],
)
def test_get_user_by_id_negative_cases(http: HttpClients, user_id, status_code):
    """
    Получение пользователя по несуществующему id
    :param http:
    :return:
    """
    response = http.auth_client.get_user_by_id_api(user_id)
    assert_status_code(response, status_code)


def test_login_user(http: HttpClients, function_user: FunctionUser):
    """
    Проверка логина пользователя с валидными данными
    :param http:
    :param function_user:
    :return:
    """
    request = LoginUserRequestSchema(
        email=function_user.email(), password=function_user.password()
    )
    response = http.auth_client.login_user_api(request)
    assert_status_code(response, 200)
    response_data = LoginUserResponseSchema.model_validate_json(response.text)
    assert_login_user_response(function_user, response_data)


def test_login_user_with_invalid_password(
    http: HttpClients, function_user: FunctionUser
):
    """
    проверка логина польлователя с валидныи email и невалидным паролем
    :param http:
    :param function_user:
    :return:
    """
    wrong_password = function_user.password() + "wrong"
    request = LoginUserRequestSchema(
        email=function_user.email(), password=wrong_password
    )
    response = http.auth_client.login_user_api(request)
    assert_status_code(response, 401)
