import uuid

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.deps import get_current_student
from db.models import InviteStatus, JoinRequest, User
from db.session import get_session
from schemas.invite import InviteCreate, InviteResponse
from services.invite_service import send_invite, update_invite_status

router = APIRouter()


@router.post("/", response_model=InviteResponse)
def create_invite(
    invite_in: InviteCreate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_student),
):
    return send_invite(db, invite_in, current_user)


@router.get("/incoming", response_model=list[InviteResponse])
def get_incoming_invites(
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_student),
):
    # Get invites sent to the user OR the user's team
    if current_user.team_id:
        return db.exec(
            select(JoinRequest).where(
                JoinRequest.target_team_id == current_user.team_id
            )
        ).all()
    else:
        return db.exec(
            select(JoinRequest).where(JoinRequest.target_user_id == current_user.id)
        ).all()


@router.put("/{invite_id}/accept", response_model=InviteResponse)
def accept_invite(
    invite_id: uuid.UUID,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_student),
):
    return update_invite_status(db, invite_id, InviteStatus.Accepted, current_user)


@router.put("/{invite_id}/reject", response_model=InviteResponse)
def reject_invite(
    invite_id: uuid.UUID,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_student),
):
    return update_invite_status(db, invite_id, InviteStatus.Rejected, current_user)
