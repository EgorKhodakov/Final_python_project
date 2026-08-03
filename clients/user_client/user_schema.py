from faker import Faker
from pydantic import BaseModel, Field

fake = Faker()

class BaseUserSchema(BaseModel):
    """
    Базовая структура пользователя
    """
    id: str
    email: str
    name: str
    createdAt: str
    role: str


class CreateUserRequestShema(BaseModel):
    """
    Описание структуры запроса на создание пользователя
    """
    email: str = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
    name: str = Field(default_factory=fake.name)


class CreateUserResponseSchema(BaseModel):
    """
    Описание структуры ответа на создание пользователя
    """
    user: BaseUserSchema
    accessToken: str


class LoginUserRequestSchema(BaseModel):
    """
    Описание структуры запроса на авторизацию пользователя
    """
    email: str = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)



class LoginUserResponseSchema(BaseModel):
    """
    Описание структуры ответа на авторизацию пользователя
    """
    user: BaseUserSchema
    accessToken: str


class GetUserResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение пользователя по id
    """
    user: BaseUserSchema
