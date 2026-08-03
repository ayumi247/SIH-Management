import uuid

from pydantic import BaseModel


class CollegeResponse(BaseModel):
    id: uuid.UUID
    name: str
    is_active: bool

    class Config:
        from_attributes = True
