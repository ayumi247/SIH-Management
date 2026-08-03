import uuid

from sqlmodel import Session

from core.exceptions import (
    BadRequestException,
    NotFoundException,
    RateLimitExceededException,
)
from core.rate_limit import check_invite_rate_limit
from db.models import InviteStatus, JoinRequest, Team, User
from schemas.invite import InviteCreate
from services.team_service import add_user_to_team


def send_invite(db: Session, invite_in: InviteCreate, sender: User) -> JoinRequest:
    if not check_invite_rate_limit(db, sender.id):
        raise RateLimitExceededException()
        
    if not invite_in.target_user_id and not invite_in.target_team_id:
        raise BadRequestException(detail="Must specify target user or target team")
        
    if invite_in.target_user_id:
        target_user = db.get(User, invite_in.target_user_id)
        if not target_user or target_user.college_id != sender.college_id:
            raise NotFoundException(detail="Target user not found or in different college")
        if not sender.team_id:
            raise BadRequestException(detail="You must be in a team to invite users")
        if target_user.id == sender.id:
            raise BadRequestException(detail="You cannot invite yourself")
        if target_user.team_id:
            raise BadRequestException(detail="User is already in a team")
            
        req = JoinRequest(
            sender_id=sender.id,
            target_user_id=target_user.id,
            target_team_id=sender.team_id
        )
    else:
        target_team = db.get(Team, invite_in.target_team_id)
        if not target_team or target_team.college_id != sender.college_id:
            raise NotFoundException(detail="Target team not found or in different college")
        if sender.team_id:
            raise BadRequestException(detail="You are already in a team")
        if len(target_team.members) >= 6:
            raise BadRequestException(detail="Team is already full")
            
        req = JoinRequest(
            sender_id=sender.id,
            target_team_id=target_team.id
        )
        
    db.add(req)
    db.commit()
    db.refresh(req)
    return req

def update_invite_status(db: Session, invite_id: uuid.UUID, new_status: InviteStatus, current_user: User):
    req = db.get(JoinRequest, invite_id)
    if not req:
        raise NotFoundException(detail="Invite not found")
        
    if req.status != InviteStatus.Pending:
        raise BadRequestException(detail="Invite already resolved")
        
    if req.target_user_id:
        # Invite was sent TO a user
        if req.target_user_id != current_user.id:
            raise BadRequestException(detail="Not authorized to resolve this invite")
    else:
        # Invite was sent TO a team
        if current_user.team_id != req.target_team_id:
            raise BadRequestException(detail="Not authorized to resolve this invite")
            
    req.status = new_status
    if new_status == InviteStatus.Accepted:
        if req.target_user_id:
            add_user_to_team(db, req.target_team_id, current_user)
        else:
            add_user_to_team(db, req.target_team_id, req.sender)
            
    db.add(req)
    db.commit()
    db.refresh(req)
    return req
