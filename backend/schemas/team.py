import uuid

from pydantic import BaseModel, ConfigDict

from db.models import TeamStatus
from schemas.user import UserResponse


class TeamCreate(BaseModel):
    name: str
    problem_statement_id: str | None = None
    required_skills: str


class TeamUpdate(BaseModel):
    name: str | None = None
    problem_statement_id: str | None = None
    required_skills: str | None = None


class TeamResponse(BaseModel):
    id: uuid.UUID
    name: str
    problem_statement_id: str | None = None
    required_skills: str
    status: TeamStatus
    college_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class TeamWithMembersResponse(TeamResponse):
    members: list[UserResponse]
