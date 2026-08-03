from fastapi import Depends, HTTPException, status, Request
from jose import jwt, JWTError
from sqlmodel import Session
from core.config import settings
from db.models import User, Role
from db.session import get_session

def get_token_from_cookie(request: Request) -> str:
    auth_cookie = request.cookies.get("access_token")
    if not auth_cookie:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    
    try:
        scheme, token = auth_cookie.split()
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth credentials")
        return token
    except ValueError:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid auth credentials")

def get_current_user(
    db: Session = Depends(get_session), token: str = Depends(get_token_from_cookie)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
        
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def get_current_student(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != Role.User:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only students can perform this action")
    return current_user

def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != Role.Admin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")
    return current_user

def get_current_super_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != Role.SuperAdmin:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")
    return current_user
