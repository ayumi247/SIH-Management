import uuid

from pydantic import BaseModel

from db.models import TeamStatus
from schemas.user import UserResponse


class TeamCreate(BaseModel):
    name: str
    problem_statement_id: str
    required_skills: str

class TeamResponse(BaseModel):
    id: uuid.UUID
    name: str
    problem_statement_id: str
    required_skills: str
    status: TeamStatus
    college_id: uuid.UUID
    
    class Config:
        from_attributes = True

class TeamWithMembersResponse(TeamResponse):
    members: list[UserResponse]
