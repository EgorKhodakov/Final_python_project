from assertions.base_assert import assert_status_code
from assertions.user_asserts import assert_create_user_response, assert_get_user_response, assert_login_user_response
from clients.auth_client.user_schema import CreateUserShema, LoginUserShema, CreateUserResponseSchema, UserSchema
from clients.http_clients import HttpClients
from fixtures.users import FunctionUser


def test_create_user(http: HttpClients):
    """
    Создание пользователя
    :param http:
    :return:
    """
    request = CreateUserShema()
    response = http.auth_client.create_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)
    assert_status_code(response, 200)
    assert_create_user_response(request, response_data)


def test_user_by_id(http: HttpClients, function_user: FunctionUser):
    """
    Получение пользователя по id
    :param http:
    :param function_user:
    :return:
    """
    user_id = function_user.id()
    response = http.auth_client.get_user_by_id_api(user_id)
    response_data = UserSchema.model_validate_json(response.text)
    assert_status_code(response, 200)
    assert_get_user_response(function_user, response_data)



def test_login_user(http: HttpClients, function_user: FunctionUser):
    """
    Авторизация пользователя
    :param http:
    :param function_user:
    :return:
    """
    request = LoginUserShema(
        email=function_user.email(), password=function_user.password()
    )
    response = http.auth_client.login_user_api(request)
    response_data = CreateUserResponseSchema.model_validate_json(response.text)
    assert_status_code(response, 200)
    assert_login_user_response(function_user, response_data.user)


def test_login_user_with_wrong_password(http: HttpClients, function_user: FunctionUser):
    """
    Авторизация пользователя с неправильным паролем
    :param http:
    :param function_user:
    :return:
    """
    request = LoginUserShema(
        email=function_user.email(),
    )  # фикстура генерирует фейковые данные
    response = http.auth_client.login_user_api(request)
    assert_status_code(response, 401)


def test_login_user_with_wrong_email(http: HttpClients, function_user: FunctionUser):
    """
    Авторизация пользователя с неправильным email
    :param http:
    :param function_user:
    :return:
    """
    request = LoginUserShema(
        password=function_user.password(),
    )  # фикстура генерирует фейковые данные
    response = http.auth_client.login_user_api(request)
    assert_status_code(response, 401)


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
