import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlmodel import Session, select

from api.deps import get_current_admin
from db.models import Team, TeamStatus, User
from db.session import get_session
from schemas.team import TeamWithMembersResponse
from services.team_service import admin_update_team_status

router = APIRouter()


@router.get("/teams", response_model=list[TeamWithMembersResponse])
def get_college_teams(
    db: Session = Depends(get_session), admin: User = Depends(get_current_admin)
):
    return db.exec(select(Team).where(Team.college_id == admin.college_id)).all()


class StatusUpdate(BaseModel):
    status: TeamStatus


@router.put("/teams/{team_id}/status", response_model=TeamWithMembersResponse)
def update_team_status(
    team_id: uuid.UUID,
    status_update: StatusUpdate,
    db: Session = Depends(get_session),
    admin: User = Depends(get_current_admin),
):
    return admin_update_team_status(db, team_id, status_update.status, admin)
