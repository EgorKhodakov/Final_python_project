from faker import Faker
from pydantic import BaseModel, ConfigDict, EmailStr, Field

fake = Faker()


class BaseUserSchema(BaseModel):
    """
    Базовая структура пользователя
    """

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(default_factory=fake.uuid4)
    email: EmailStr
    name: str
    created_at: str = Field(alias="createdAt")
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

    model_config = ConfigDict(populate_by_name=True)

    user: BaseUserSchema
    access_token: str = Field(alias="accessToken")


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

    model_config = ConfigDict(populate_by_name=True)

    user: BaseUserSchema
    access_token: str = Field(alias="accessToken")


class GetUserResponseSchema(BaseModel):
    """
    Описание структуры ответа на получение пользователя по id
    """

    user: BaseUserSchema
