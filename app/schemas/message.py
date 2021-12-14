from pydantic import BaseModel


class Message(BaseModel):
    date: str
    users: list[str]
    text: str

