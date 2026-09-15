from http import HTTPStatus

import pytest

from assertions.base_assert import assert_status_code
from assertions.user_asserts import (
    assert_create_user_response,
    assert_get_user_response,
    assert_login_user_response,
)
from clients.http_clients import HttpClients
from clients.user_client.user_schema import (
    CreateUserRequestShema,
    CreateUserResponseSchema,
    GetUserResponseSchema,
    LoginUserRequestSchema,
    LoginUserResponseSchema,
)
from fixtures.users import FunctionUser
from tools.fakers import fake

@pytest.mark.user
class TestUser:

    def test_create_user(self, http: HttpClients):
        """
        Создание пользователя
        :param http:
        :return:
        """
        request = CreateUserRequestShema()
        response = http.auth_client.create_user_api(request)
        response_data = CreateUserResponseSchema.model_validate_json(response.text)
        assert_status_code(response, HTTPStatus.OK)
        assert_create_user_response(request, response_data)

    @pytest.mark.xfail(reason="Ожидается 400 возвращает 500")
    def test_create_user_with_duplicate_email(self, http: HttpClients):
        """
        Создание пользователя дважды с одинаковыми данными
        :param http:
        :return:
        """
        request = CreateUserRequestShema()
        first_response = http.auth_client.create_user_api(request)
        assert_status_code(first_response, HTTPStatus.OK)
        second_response = http.auth_client.create_user_api(request)
        assert_status_code(second_response, HTTPStatus.BAD_REQUEST)

    @pytest.mark.parametrize(
        "email, password, name, status_code",
        [
            ("", "passwer@#$5", "egor", HTTPStatus.BAD_REQUEST),
            ("qa@email.com", "", "egor", HTTPStatus.BAD_REQUEST),
            pytest.param(
                "qa@email.com",
                "pass",
                "egor",
                HTTPStatus.BAD_REQUEST,
                marks=pytest.mark.xfail(reason="должен вернуть 200, возвращает 500"),
            ),
            pytest.param(
                "qa@email.com",
                "123456",
                "egor",
                HTTPStatus.BAD_REQUEST,
                marks=pytest.mark.xfail(reason="должен вернуть 200, возвращает 500"),
            ),
        ],
        ids=[
            "create-user_without_email",
            "create-user_without_password",
            "create-user_with_short_password",
            "create-user_with_digital_password",
        ],
    )
    def test_create_user_negative(
        self, http: HttpClients, email, password, name, status_code
    ):
        request = CreateUserRequestShema(
            email=email,
            password=password,
            name=name,
        )
        response = http.auth_client.create_user_api(request)
        assert_status_code(response, status_code)

    def test_get_user_by_id(self, http: HttpClients, function_user: FunctionUser):
        """
        Получение пользователя по id
        :param http:
        :param function_user:
        :return:
        """
        user_id = function_user.id
        response = http.auth_client.get_user_by_id_api(user_id)
        response_data = GetUserResponseSchema.model_validate_json(response.text)
        assert_status_code(response, HTTPStatus.OK)
        assert_get_user_response(function_user, response_data)

    @pytest.mark.parametrize(
        "email, password, status_code",
        [
            ("", "", HTTPStatus.BAD_REQUEST),
            ("validemail@google.com", "", HTTPStatus.BAD_REQUEST),
            ("", "validpassq34%$^", HTTPStatus.BAD_REQUEST),
            ("invalid-email", "validpassq34%$^", HTTPStatus.UNAUTHORIZED),
            ("nonexistent@yahoo.ru", "validpassq34%$^", HTTPStatus.UNAUTHORIZED),
        ],
        ids=[
            "login_without_email_and_password",
            "login_without_password",
            "login_without_email",
            "login_with_invalid_email",
            "login_with_nonexistent_email",
        ],
    )
    def test_login_user_negative(self, http: HttpClients, email, password, status_code):
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
            (fake.uid(), HTTPStatus.NOT_FOUND),
            pytest.param(
                "sdafwer423434334fv",
                HTTPStatus.BAD_REQUEST,
                marks=pytest.mark.xfail(
                    reason="некорректный запрос, ожидается 400, приходит 500"
                ),
            ),
            pytest.param(
                None,
                HTTPStatus.BAD_REQUEST,
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
    def test_get_user_by_id_negative_cases(
        self, http: HttpClients, user_id, status_code
    ):
        """
        Получение пользователя по несуществующему id
        :param http:
        :return:
        """
        response = http.auth_client.get_user_by_id_api(user_id)
        assert_status_code(response, status_code)

    def test_login_user(self, http: HttpClients, function_user: FunctionUser):
        """
        Проверка логина пользователя с валидными данными
        :param http:
        :param function_user:
        :return:
        """
        response = http.auth_client.login_user_api(function_user.valid_login_payload)
        assert_status_code(response, HTTPStatus.OK)
        response_data = LoginUserResponseSchema.model_validate_json(response.text)
        assert_login_user_response(function_user, response_data)

    def test_login_user_with_invalid_password(
        self, http: HttpClients, function_user: FunctionUser
    ):
        """
        проверка логина польлователя с валидныи email и невалидным паролем
        :param http:
        :param function_user:
        :return:
        """
        request = function_user.login_payload_with_invalid_password
        response = http.auth_client.login_user_api(request)
        assert_status_code(response, HTTPStatus.UNAUTHORIZED)

    def test_delete_user(self, http: HttpClients, function_user: FunctionUser):
        """
        Проверка удаления пользователя
        :param http:
        :param function_user: фикстура создающая пользователя
        :return:
        """
        response = http.auth_client.delete_user_api(
            function_user.id, function_user.access_token
        )
        assert_status_code(response, HTTPStatus.OK)

    def test_delete_user_twice_returns_404(
        self, http: HttpClients, function_user: FunctionUser
    ):
        """
        Проверка удаления пользователя
        :param http:
        :param function_user: фикстура создающая пользователя
        :return:
        """
        user_id = function_user.id
        access_token = function_user.access_token

        first_response = http.auth_client.delete_user_api(user_id, access_token)
        assert_status_code(first_response, HTTPStatus.OK)
        second_response = http.auth_client.delete_user_api(user_id, access_token)
        assert_status_code(second_response, HTTPStatus.NOT_FOUND)
