from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
import uuid
from db.session import get_session
from db.models import User, Role, College
from schemas.user import UserResponse
from schemas.college import CollegeResponse
from api.deps import get_current_super_admin
from services.super_admin_service import approve_admin

router = APIRouter()

@router.get("/admins/pending", response_model=List[UserResponse])
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

@router.get("/colleges", response_model=List[CollegeResponse])
def get_all_colleges(
    db: Session = Depends(get_session),
    super_admin: User = Depends(get_current_super_admin)
):
    return db.exec(select(College)).all()

from schemas.team import TeamWithMembersResponse
from db.models import Team

@router.get("/colleges/{college_id}/teams", response_model=List[TeamWithMembersResponse])
def get_college_teams(
    college_id: uuid.UUID,
    db: Session = Depends(get_session),
    super_admin: User = Depends(get_current_super_admin)
):
    return db.exec(select(Team).where(Team.college_id == college_id)).all()
