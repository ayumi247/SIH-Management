from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from db.session import get_session
from db.models import User, Team, TeamStatus
from schemas.team import TeamCreate, TeamResponse, TeamWithMembersResponse
from api.deps import get_current_user
from services.team_service import create_team
from core.exceptions import NotFoundException

router = APIRouter()

@router.post("/", response_model=TeamResponse)
def create_new_team(
    team_in: TeamCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    return create_team(db, team_in, current_user)

@router.get("/my-team", response_model=TeamWithMembersResponse)
def get_my_team(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    if not current_user.team_id:
        raise NotFoundException(detail="You are not in a team")
    team = db.get(Team, current_user.team_id)
    return team

@router.get("/available", response_model=List[TeamResponse])
def get_available_teams(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    # Fetch teams in same college that have < 6 members.
    teams = db.exec(
        select(Team).where(
            Team.college_id == current_user.college_id,
            Team.status == TeamStatus.Pending
        )
    ).all()
    # Filter those with < 6 members in memory
    return [t for t in teams if len(t.members) < 6]
