import uuid

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.deps import get_current_super_admin
from db.models import College, Role, User
from db.session import get_session
from schemas.college import CollegeResponse
from schemas.user import UserResponse
from services.super_admin_service import approve_admin

router = APIRouter()

@router.get("/admins/pending", response_model=list[UserResponse])
def get_pending_admins(
    db: Session = Depends(get_session),
    super_admin: User = Depends(get_current_super_admin)
):
    return db.exec(select(User).where(User.role == Role.Admin_Pending)).all()

@router.put("/admins/{admin_id}/approve", response_model=UserResponse)
def approve_pending_admin(
    admin_id: uuid.UUID,
    db: Session = Depends(get_session),
    super_admin: User = Depends(get_current_super_admin)
):
    return approve_admin(db, admin_id)

@router.get("/colleges", response_model=list[CollegeResponse])
def get_all_colleges(
    db: Session = Depends(get_session),
    super_admin: User = Depends(get_current_super_admin)
):
    return db.exec(select(College)).all()

from db.models import Team
from schemas.team import TeamWithMembersResponse


@router.get("/colleges/{college_id}/teams", response_model=list[TeamWithMembersResponse])
def get_college_teams(
    college_id: uuid.UUID,
    db: Session = Depends(get_session),
    super_admin: User = Depends(get_current_super_admin)
):
    return db.exec(select(Team).where(Team.college_id == college_id)).all()
