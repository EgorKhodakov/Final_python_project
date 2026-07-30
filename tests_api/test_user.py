from clients.http_clients import HttpClients
from fixtures.users import FunctionUser
from clients.auth_client.user_schema import CreateUserShema, LoginUserShema


def test_create_user(http: HttpClients):
        request = CreateUserShema()
        response = http.auth_client.create_user_api(request)
        assert response.status_code == 200


def test_user_by_id(http: HttpClients, function_user: FunctionUser):
    user_id = function_user.id()
    response = http.auth_client.get_user_by_id_api(user_id)
    assert response.status_code == 200


def test_login_user(http: HttpClients, function_user: FunctionUser):
    request = LoginUserShema(
        email=function_user.email(),
        password=function_user.password()
    )
    response = http.auth_client.login_user_api(request)
    assert response.status_code == 200
