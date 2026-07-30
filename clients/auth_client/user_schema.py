from pydantic import BaseModel, Field
from faker import Faker

fake = Faker()


class UserSchema(BaseModel):
    id: str
    email: str
    name: str
    createdAt: str
    role: str


class CreateUserShema(BaseModel):
    """
    Модель запроса для создания пользователя
    """

    email: str = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
    name: str = Field(default_factory=fake.name)


class CreateUserResponseSchema(BaseModel):
    user: UserSchema
    accessToken: str


class LoginUserShema(BaseModel):
    email: str = Field(default_factory=fake.email)
    password: str = Field(default_factory=fake.password)
