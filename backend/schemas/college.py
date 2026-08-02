from pydantic import BaseModel
import uuid

class CollegeResponse(BaseModel):
    id: uuid.UUID
    name: str
    is_active: bool
    
    class Config:
        from_attributes = True
