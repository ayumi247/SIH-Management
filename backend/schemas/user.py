import uuid

from pydantic import BaseModel, EmailStr, ConfigDict

from db.models import Role


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone: str
    enrollment_no: str
    year: str
    branch: str
    gender: str
    skills: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None
    college_id: uuid.UUID


class AdminCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    phone: str
    enrollment_no: str
    year: str
    branch: str
    gender: str
    position: str
    college_name: str


class UserUpdate(BaseModel):
    github_url: str | None = None
    linkedin_url: str | None = None
    skills: str | None = None


class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    phone: str
    enrollment_no: str
    year: str
    branch: str
    gender: str
    skills: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None
    position: str | None = None
    role: Role
    college_id: uuid.UUID
    team_id: uuid.UUID | None = None
    team_name: str | None = None

    model_config = ConfigDict(from_attributes=True)
