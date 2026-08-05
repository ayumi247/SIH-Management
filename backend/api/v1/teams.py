from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.deps import get_current_student
from core.exceptions import NotFoundException
from db.models import Team, TeamStatus, User
from db.session import get_session
from schemas.team import TeamCreate, TeamResponse, TeamUpdate, TeamWithMembersResponse
from services.team_service import create_team

router = APIRouter()


@router.post("/", response_model=TeamResponse)
def create_new_team(
    team_in: TeamCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_student),
):
    return create_team(db, team_in, current_user)


@router.patch("/my-team", response_model=TeamResponse)
def update_my_team(
    team_update: TeamUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_student),
):
    if not current_user.team_id:
        raise NotFoundException(detail="You are not in a team")

    team = db.get(Team, current_user.team_id)
    if not team:
        raise NotFoundException(detail="Team not found")

    update_data = team_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(team, key, value)

    db.add(team)
    db.commit()
    db.refresh(team)
    return team


@router.get("/my-team", response_model=TeamWithMembersResponse)
def get_my_team(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_student),
):
    if not current_user.team_id:
        raise NotFoundException(detail="You are not in a team")
    team = db.get(Team, current_user.team_id)
    return team


@router.get("/available", response_model=list[TeamWithMembersResponse])
def get_available_teams(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_student),
):
    # Fetch teams in same college that have < 6 members.
    teams = db.exec(
        select(Team).where(
            Team.college_id == current_user.college_id,
            Team.status == TeamStatus.Pending,
        )
    ).all()
    # Filter those with < 6 members in memory
    return [t for t in teams if len(t.members) < 6]


@router.post("/leave")
def leave_team(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_student),
):
    if not current_user.team_id:
        raise NotFoundException(detail="You are not in a team")

    team = db.get(Team, current_user.team_id)
    if not team:
        raise NotFoundException(detail="Team not found")

    if team.leader_id == current_user.id:
        from core.exceptions import BadRequestException

        raise BadRequestException(
            detail="Team leaders cannot leave the team, they can only delete it"
        )

    current_user.team_id = None
    db.add(current_user)
    db.commit()
    return {"message": "Successfully left the team"}


@router.delete("/my-team")
def delete_my_team(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_student),
):
    if not current_user.team_id:
        raise NotFoundException(detail="You are not in a team")

    team = db.get(Team, current_user.team_id)
    if not team:
        raise NotFoundException(detail="Team not found")

    if team.leader_id != current_user.id:
        from core.exceptions import BadRequestException

        raise BadRequestException(detail="Only the team leader can delete the team")

    # Kick all members
    for member in team.members:
        member.team_id = None
        db.add(member)

    # Delete the team
    db.delete(team)
    db.commit()

    return {"message": "Team deleted successfully"}
