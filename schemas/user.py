from pydantic import BaseModel


class UserInSchema(BaseModel):
    username: str
    password: str


class UserOutSchema(BaseModel):
    name: str

