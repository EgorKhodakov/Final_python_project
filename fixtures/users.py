from pydantic import BaseModel
import pytest

from clients.auth_client.user_schema import CreateUserShema, CreateUserResponseSchema


class FunctionUser(BaseModel):
    request: CreateUserShema
    response: CreateUserResponseSchema

    def id(self) -> str:
        return self.response.user.id

    def password(self) -> str:
        return self.request.password

    def email(self) -> str:
        return self.request.email

    def access_token(self) -> str:
        return self.response.accessToken


@pytest.fixture(scope="function")
def function_user(http) -> FunctionUser:
    request = CreateUserShema()
    response = http.auth_client.create_user(request)
    return FunctionUser(request=request, response=response)
