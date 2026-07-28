from pydantic import BaseModel


class CreateOrderSchema(BaseModel):
    user_id: str


class RefreshOrderSchema(BaseModel):
    fromStatus: str
    toStatus: str
