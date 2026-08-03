
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.deps import get_current_student
from core.exceptions import NotFoundException
from db.models import Team, TeamStatus, User
from db.session import get_session
from schemas.team import TeamCreate, TeamResponse, TeamWithMembersResponse
from services.team_service import create_team

router = APIRouter()

@router.post("/", response_model=TeamResponse)
def create_new_team(
    team_in: TeamCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_student)
):
    return create_team(db, team_in, current_user)

@router.get("/my-team", response_model=TeamWithMembersResponse)
def get_my_team(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_student)
):
    if not current_user.team_id:
        raise NotFoundException(detail="You are not in a team")
    team = db.get(Team, current_user.team_id)
    return team

@router.get("/available", response_model=list[TeamResponse])
def get_available_teams(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_student)
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
