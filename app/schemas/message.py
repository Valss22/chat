from bson import ObjectId
from pydantic import BaseModel, Field

from app.schemas.user import PyObjectId


class Message(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    text: str
    is_mine: bool = Field(alias='isMine')

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
