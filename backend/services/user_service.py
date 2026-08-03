from sqlmodel import Session, select

from core.exceptions import NotFoundException
from db.models import Role, User


def get_user_by_id(db: Session, user_id: str) -> User:
    user = db.get(User, user_id)
    if not user:
        raise NotFoundException(detail="User not found")
    return user


def get_available_teammates(db: Session, college_id: str):
    statement = select(User).where(
        User.college_id == college_id, User.role == Role.User, User.team_id == None
    )
    return db.exec(statement).all()
