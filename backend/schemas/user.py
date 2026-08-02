from pydantic import BaseModel, EmailStr
from typing import Optional
import uuid
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
    skills: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
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
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    skills: Optional[str] = None

class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    name: str
    phone: str
    enrollment_no: str
    year: str
    branch: str
    gender: str
    skills: Optional[str] = None
    github_url: Optional[str] = None
    linkedin_url: Optional[str] = None
    position: Optional[str] = None
    role: Role
    college_id: uuid.UUID
    team_id: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True
