import pytest
import httpx
from pydantic import BaseModel

from clients.http_clients import HttpClients

from data.urls import BASE_URL
from schemas.user_schema import CreateUserResponseSchema, CreateUserShema


class FunctionUser(BaseModel):
    request: CreateUserShema
    response: CreateUserResponseSchema

    def id(self) -> str:
        return self.response.user.id


    def password(self) -> str:
        return self.request.password


    def email(self) -> str:
        return self.request.email


@pytest.fixture(scope="session")
def http():
    with httpx.Client(base_url=BASE_URL) as client:
        api_facade = HttpClients(client)
        yield api_facade



@pytest.fixture(scope="function")
def function_user(http) -> FunctionUser:
    request = CreateUserShema()
    response = http.auth_client.create_user(request)
    return FunctionUser(request=request, response=response)

