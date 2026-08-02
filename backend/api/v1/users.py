from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from typing import List
from db.session import get_session
from db.models import User, College
from schemas.user import UserResponse, UserUpdate
from schemas.college import CollegeResponse
from api.deps import get_current_user
from services.user_service import get_available_teammates

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.patch("/me", response_model=UserResponse)
def update_me(
    user_update: UserUpdate,
    db: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(current_user, key, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me")
def delete_me(db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    # Simple delete for MVP
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted successfully"}

@router.get("/teammates", response_model=List[UserResponse])
def search_teammates(
    db: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    return get_available_teammates(db, str(current_user.college_id))

@router.get("/colleges/active", response_model=List[CollegeResponse])
def get_active_colleges(db: Session = Depends(get_session)):
    return db.exec(select(College).where(College.is_active == True)).all()

@router.get("/colleges", response_model=List[CollegeResponse])
def get_all_colleges(db: Session = Depends(get_session)):
    return db.exec(select(College)).all()

@router.get("/eligible", response_model=List[UserResponse])
def get_eligible_students(db: Session = Depends(get_session), current_user: User = Depends(get_current_user)):
    return db.exec(
        select(User).where(
            User.college_id == current_user.college_id,
            User.team_id == None,
            User.role == "User",
            User.id != current_user.id
        )
    ).all()
