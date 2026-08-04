from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from api.deps import get_current_user
from core.exceptions import BadRequestException
from db.models import College, Team, TeamStatus, User
from db.session import get_session
from schemas.college import CollegeResponse
from schemas.user import UserResponse, UserUpdate
from services.user_service import get_available_teammates

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_me(
    user_update: UserUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user),
):
    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(current_user, key, value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


@router.delete("/me")
def delete_me(
    db: Session = Depends(get_session), current_user: User = Depends(get_current_user)
):
    if current_user.team_id:
        team = db.get(Team, current_user.team_id)
        if team:
            if team.status != TeamStatus.Pending:
                raise BadRequestException(
                    detail="Cannot delete account while your team is Shortlisted or Waitlisted."
                )
            # If the user is the only member, delete the team entirely
            if len(team.members) == 1:
                db.delete(team)

    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted successfully"}


@router.get("/teammates", response_model=list[UserResponse])
def search_teammates(
    db: Session = Depends(get_session), current_user: User = Depends(get_current_user)
):
    return get_available_teammates(db, str(current_user.college_id))


@router.get("/colleges/active", response_model=list[CollegeResponse])
def get_active_colleges(db: Session = Depends(get_session)):
    return db.exec(select(College).where(College.is_active == True)).all()


@router.get("/colleges", response_model=list[CollegeResponse])
def get_all_colleges(db: Session = Depends(get_session)):
    return db.exec(select(College)).all()


@router.get("/eligible", response_model=list[UserResponse])
def get_eligible_students(
    db: Session = Depends(get_session), current_user: User = Depends(get_current_user)
):
    return db.exec(
        select(User).where(
            User.college_id == current_user.college_id,
            User.team_id == None,
            User.role == "User",
            User.id != current_user.id,
        )
    ).all()


@router.get("/college-members", response_model=list[UserResponse])
def get_college_members(
    db: Session = Depends(get_session), current_user: User = Depends(get_current_user)
):
    return db.exec(
        select(User).where(
            User.college_id == current_user.college_id,
            User.id != current_user.id,
        )
    ).all()
