import uuid

from pydantic import BaseModel, ConfigDict


class CollegeResponse(BaseModel):
    id: uuid.UUID
    name: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
