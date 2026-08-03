import uuid

from sqlmodel import Session

from core.exceptions import NotFoundException
from db.models import College, Role, User


def approve_admin(db: Session, admin_id: uuid.UUID) -> User:
    admin = db.get(User, admin_id)
    if not admin or admin.role != Role.Admin_Pending:
        raise NotFoundException(detail="Pending admin not found")
        
    admin.role = Role.Admin
    
    college = db.get(College, admin.college_id)
    college.is_active = True
    
    db.add(admin)
    db.add(college)
    db.commit()
    db.refresh(admin)
    return admin
