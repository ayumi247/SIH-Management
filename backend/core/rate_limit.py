from datetime import datetime, timedelta, timezone

from sqlmodel import Session, select

from db.models import JoinRequest


def check_invite_rate_limit(db: Session, user_id: str) -> bool:
    """Returns True if user is under the rate limit (5 invites per minute), False otherwise."""
    one_minute_ago = datetime.now(timezone.utc) - timedelta(minutes=1)

    # Count requests sent by this user in the last minute
    statement = select(JoinRequest).where(
        JoinRequest.sender_id == user_id, JoinRequest.created_at >= one_minute_ago
    )
    recent_requests = db.exec(statement).all()

    return len(recent_requests) < 5
