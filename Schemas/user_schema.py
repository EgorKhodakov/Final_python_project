from pydantic import BaseModel


class CreateUserShema(BaseModel):
    """
    Модель запроса для создания пользователя
    """

    email: str
    password: str
    name: str
