from bson import ObjectId
from pydantic import BaseModel, Field

from app.schemas.user import PyObjectId


class Dialog(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias='_id')
    username: str = Field(alias='name')

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
