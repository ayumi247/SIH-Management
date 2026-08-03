from sqlmodel import Session, select

from core.exceptions import BadRequestException, UnauthorizedException
from core.security import get_password_hash, verify_password
from db.models import College, Role, User
from schemas.user import AdminCreate, UserCreate


def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.exec(select(User).where(User.email == email)).first()
    if not user:
        raise UnauthorizedException(detail="Incorrect email or password")
    if not verify_password(password, user.hashed_password):
        raise UnauthorizedException(detail="Incorrect email or password")
    return user


def create_user(db: Session, user_in: UserCreate) -> User:
    user = db.exec(select(User).where(User.email == user_in.email)).first()
    if user:
        raise BadRequestException(detail="Email already registered")

    college = db.exec(select(College).where(College.id == user_in.college_id)).first()
    if not college or not college.is_active:
        raise BadRequestException(detail="Invalid or inactive college")

    new_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        name=user_in.name,
        phone=user_in.phone,
        enrollment_no=user_in.enrollment_no,
        year=user_in.year,
        branch=user_in.branch,
        gender=user_in.gender,
        skills=user_in.skills,
        github_url=user_in.github_url,
        linkedin_url=user_in.linkedin_url,
        college_id=user_in.college_id,
        role=Role.User,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def create_admin_request(db: Session, admin_in: AdminCreate) -> User:
    user = db.exec(select(User).where(User.email == admin_in.email)).first()
    if user:
        raise BadRequestException(detail="Email already registered")

    # Find or create college
    college = db.exec(
        select(College).where(College.name == admin_in.college_name)
    ).first()
    if not college:
        college = College(name=admin_in.college_name, is_active=False)
        db.add(college)
        db.commit()
        db.refresh(college)

    existing_admin = db.exec(
        select(User).where(
            User.college_id == college.id,
            User.role.in_([Role.Admin, Role.Admin_Pending]),
        )
    ).first()

    if existing_admin:
        raise BadRequestException(
            detail="College already has an Admin or pending Admin request"
        )

    admin = User(
        email=admin_in.email,
        hashed_password=get_password_hash(admin_in.password),
        name=admin_in.name,
        phone=admin_in.phone,
        enrollment_no=admin_in.enrollment_no,
        year=admin_in.year,
        branch=admin_in.branch,
        gender=admin_in.gender,
        position=admin_in.position,
        college_id=college.id,
        role=Role.Admin_Pending,
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    return admin
