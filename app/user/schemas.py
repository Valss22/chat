from pydantic import BaseModel


class UserIn(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: str
    email: str
    jwt: str
