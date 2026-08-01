from clients.auth_client.user_schema import CreateUserShema, CreateUserResponseSchema, UserSchema, User
from clients.http_clients import HttpClients
from assertions.base_assert import assert_status_code
from fixtures.users import FunctionUser


def assert_create_user_response(request: CreateUserShema, response: CreateUserResponseSchema):
    assert request.email == response.user.email
    assert request.name == response.user.name
    assert response.accessToken is not None


def assert_get_user_response(request: FunctionUser, response: UserSchema):
    assert request.id() == response.user.id
    assert request.email() == response.user.email
    assert request.response.user.name == response.user.name
    assert request.response.user.createdAt == response.user.createdAt
    assert request.response.user.role == response.user.role


def assert_login_user_response(request: FunctionUser, response: User):
    assert request.id() == response.id
    assert request.email() == response.email
    assert request.response.user.name == response.name
    assert request.response.user.createdAt == response.createdAt
    assert request.response.user.role == response.role