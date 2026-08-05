import uuid
from datetime import datetime, timezone
from enum import Enum as PyEnum

from sqlmodel import Field, Relationship, SQLModel


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

    users: list["User"] = Relationship(back_populates="college")
    teams: list["Team"] = Relationship(back_populates="college")


class Team(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    problem_statement_id: str | None = None
    required_skills: str
    status: TeamStatus = Field(default=TeamStatus.Pending)
    college_id: uuid.UUID = Field(foreign_key="college.id")
    leader_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")

    college: College = Relationship(back_populates="teams")
    members: list["User"] = Relationship(
        back_populates="team",
        sa_relationship_kwargs={
            "foreign_keys": "[User.team_id]",
        },
    )
    join_requests: list["JoinRequest"] = Relationship(back_populates="target_team")


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
    skills: str | None = None
    github_url: str | None = None
    linkedin_url: str | None = None
    position: str | None = None

    college_id: uuid.UUID = Field(foreign_key="college.id")
    team_id: uuid.UUID | None = Field(default=None, foreign_key="team.id")

    college: College = Relationship(back_populates="users")
    team: Team | None = Relationship(
        back_populates="members",
        sa_relationship_kwargs={
            "foreign_keys": "[User.team_id]",
        },
    )
    led_teams: list[Team] = Relationship(
        sa_relationship_kwargs={
            "primaryjoin": "User.id == Team.leader_id",
            "foreign_keys": "[Team.leader_id]",
        }
    )

    sent_requests: list["JoinRequest"] = Relationship(
        back_populates="sender",
        sa_relationship_kwargs={
            "foreign_keys": "[JoinRequest.sender_id]",
            "cascade": "all, delete-orphan",
        },
    )
    received_requests: list["JoinRequest"] = Relationship(
        back_populates="target_user",
        sa_relationship_kwargs={
            "foreign_keys": "[JoinRequest.target_user_id]",
            "cascade": "all, delete-orphan",
        },
    )

    @property
    def team_name(self) -> str | None:
        return self.team.name if self.team else None


class JoinRequest(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    sender_id: uuid.UUID = Field(foreign_key="user.id")
    target_team_id: uuid.UUID | None = Field(default=None, foreign_key="team.id")
    target_user_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")
    status: InviteStatus = Field(default=InviteStatus.Pending)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    sender: User = Relationship(
        back_populates="sent_requests",
        sa_relationship_kwargs={"foreign_keys": "[JoinRequest.sender_id]"},
    )
    target_team: Team | None = Relationship(back_populates="join_requests")
    target_user: User | None = Relationship(
        back_populates="received_requests",
        sa_relationship_kwargs={"foreign_keys": "[JoinRequest.target_user_id]"},
    )

    @property
    def sender_name(self) -> str | None:
        return self.sender.name if self.sender else None

    @property
    def target_team_name(self) -> str | None:
        return self.target_team.name if self.target_team else None

    @property
    def sender_team_name(self) -> str | None:
        return self.sender.team.name if (self.sender and self.sender.team) else None

    @property
    def target_user_name(self) -> str | None:
        return self.target_user.name if self.target_user else None
