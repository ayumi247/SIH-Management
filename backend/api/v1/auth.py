from fastapi import APIRouter, Depends, Response
from sqlmodel import Session
from db.session import get_session
from schemas.user import UserCreate, AdminCreate, UserResponse
from services.auth_service import authenticate_user, create_user, create_admin_request
from core.security import create_access_token
from pydantic import BaseModel

router = APIRouter()

class LoginData(BaseModel):
    email: str
    password: str

@router.post("/login")
def login(data: LoginData, db: Session = Depends(get_session)):
    user = authenticate_user(db, data.email, data.password)
    access_token = create_access_token(subject=user.id)
    return {"message": "Logged in successfully", "role": user.role, "access_token": access_token}

@router.post("/register", response_model=UserResponse)
def register_user(user_in: UserCreate, db: Session = Depends(get_session)):
    return create_user(db, user_in)

@router.post("/register/admin", response_model=UserResponse)
def register_admin(admin_in: AdminCreate, db: Session = Depends(get_session)):
    return create_admin_request(db, admin_in)
    
@router.post("/logout")
def logout():
    return {"message": "Logged out successfully"}
