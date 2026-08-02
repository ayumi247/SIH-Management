from pydantic import BaseModel
from typing import Optional
import uuid
from db.models import InviteStatus

class InviteCreate(BaseModel):
    target_user_id: Optional[uuid.UUID] = None
    target_team_id: Optional[uuid.UUID] = None

class InviteResponse(BaseModel):
    id: uuid.UUID
    sender_id: uuid.UUID
    target_team_id: Optional[uuid.UUID]
    target_user_id: Optional[uuid.UUID]
    status: InviteStatus
    
    class Config:
        from_attributes = True
