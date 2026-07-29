from pydantic import BaseModel


class LoginUserSchema(BaseModel):
    """
    Модель логина пользователя
    """

    email: str
    password: str
