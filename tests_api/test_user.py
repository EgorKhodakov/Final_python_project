import pytest

from assertions.base_assert import assert_status_code
from assertions.user_asserts import assert_create_user_response, assert_get_user_response, assert_login_user_response
from clients.user_client.user_schema import CreateUserRequestShema, LoginUserRequestSchema,\
    CreateUserResponseSchema, GetUserResponseSchema, LoginUserResponseSchema
from clients.http_clients import HttpClients
from fixtures.users import FunctionUser


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


@pytest.mark.parametrize("email, password, status_code", [
    (None, None, 200),
    (None, "123rSDer3", 401),
    ("asdgsrsd", None, 401),
    ("", "", 400),
    (None, "", 400),
    ("", None, 400)
], ids=[
    "login_cuccess",
    "login_with_wrong_password",
    "login_with_wrong_email",
    "login_without_email_and_password",
    "login_without_email",
    "login_without_password"

])
def test_login_user(http: HttpClients, function_user: FunctionUser, email, password, status_code):
    """
    Авторизация пользователя
    :param http:
    :param function_user:
    :return:
    """
    email = email if email is not None else function_user.email()
    password = password if password is not None else function_user.password()
    request = LoginUserRequestSchema(
        email=email, password=password
    )
    response = http.auth_client.login_user_api(request)

    assert_status_code(response, status_code)
    if response.status_code == 200:
        response_data = LoginUserResponseSchema.model_validate_json(response.text)
        assert_login_user_response(function_user, response_data)


def test_user_with_incorrect_id(http: HttpClients, function_user: FunctionUser):
    """
    Получение пользователя по несуществующему id
    :param http:
    :param function_user:
    :return:
    """
    user_id = "sdafwer423434334fv"
    response = http.auth_client.get_user_by_id_api(user_id)
    assert_status_code(response, 500)
