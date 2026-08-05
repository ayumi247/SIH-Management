import uuid

from pydantic import BaseModel, ConfigDict

from db.models import InviteStatus


class InviteCreate(BaseModel):
    target_user_id: uuid.UUID | None = None
    target_team_id: uuid.UUID | None = None


class InviteResponse(BaseModel):
    id: uuid.UUID
    sender_id: uuid.UUID
    target_team_id: uuid.UUID | None
    target_user_id: uuid.UUID | None
    status: InviteStatus

    sender_name: str | None = None
    target_team_name: str | None = None
    sender_team_name: str | None = None
    target_user_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
