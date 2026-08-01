from faker import Faker
from pydantic import BaseModel, Field

fake = Faker()

class User(BaseModel):
    id: str
    email: str
    name: str
    createdAt: str
    role: str


class UserSchema(BaseModel):
    user: User


class CreateUserShema(BaseModel):
    """
    Модель запроса для создания пользователя
    """

    email: str = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
    name: str = Field(default_factory=fake.name)


class CreateUserResponseSchema(BaseModel):
    user: User
    accessToken: str


class LoginUserShema(BaseModel):
    email: str = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
