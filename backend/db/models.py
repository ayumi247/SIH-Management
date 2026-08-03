import uuid
from typing import Optional, List
from datetime import datetime
from sqlmodel import Field, SQLModel, Relationship
from enum import Enum as PyEnum

class Role(str, PyEnum):
    User = "User"
    Admin_Pending = "Admin_Pending"
    Admin = "Admin"
    SuperAdmin = "SuperAdmin"

class TeamStatus(str, PyEnum):
    Pending = "Pending"
    Shortlisted = "Shortlisted"
    Waitlisted = "Waitlisted"

class InviteStatus(str, PyEnum):
    Pending = "Pending"
    Accepted = "Accepted"
    Rejected = "Rejected"

class College(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(unique=True, index=True)
    is_active: bool = Field(default=False)
    
    users: List["User"] = Relationship(back_populates="college")
    teams: List["Team"] = Relationship(back_populates="college")

class Team(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    problem_statement_id: str
    required_skills: str
    status: TeamStatus = Field(default=TeamStatus.Pending)
    college_id: uuid.UUID = Field(foreign_key="college.id")
    
    college: College = Relationship(back_populates="teams")
    members: List["User"] = Relationship(back_populates="team")
    join_requests: List["JoinRequest"] = Relationship(back_populates="target_team")

class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    hashed_password: str
    role: Role = Field(default=Role.User)
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
    
    college_id: uuid.UUID = Field(foreign_key="college.id")
    team_id: Optional[uuid.UUID] = Field(default=None, foreign_key="team.id")
    
    college: College = Relationship(back_populates="users")
    team: Optional[Team] = Relationship(back_populates="members")
    
    sent_requests: List["JoinRequest"] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs={"foreign_keys": "[JoinRequest.sender_id]", "cascade": "all, delete-orphan"}
    )
    received_requests: List["JoinRequest"] = Relationship(
        back_populates="target_user",
        sa_relationship_kwargs={"foreign_keys": "[JoinRequest.target_user_id]", "cascade": "all, delete-orphan"}
    )

class JoinRequest(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sender_id: uuid.UUID = Field(foreign_key="user.id")
    target_team_id: Optional[uuid.UUID] = Field(default=None, foreign_key="team.id")
    target_user_id: Optional[uuid.UUID] = Field(default=None, foreign_key="user.id")
    status: InviteStatus = Field(default=InviteStatus.Pending)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    sender: User = Relationship(
        back_populates="sent_requests",
        sa_relationship_kwargs={"foreign_keys": "[JoinRequest.sender_id]"}
    )
    target_team: Optional[Team] = Relationship(back_populates="join_requests")
    target_user: Optional[User] = Relationship(
        back_populates="received_requests",
        sa_relationship_kwargs={"foreign_keys": "[JoinRequest.target_user_id]"}
    )
