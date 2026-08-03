import uuid

from sqlmodel import Session, select

from core.exceptions import BadRequestException, NotFoundException
from db.models import Team, TeamStatus, User
from schemas.team import TeamCreate


def create_team(db: Session, team_in: TeamCreate, user: User) -> Team:
    if user.team_id:
        raise BadRequestException(detail="User is already in a team")

    team = db.exec(
        select(Team).where(
            Team.name == team_in.name, Team.college_id == user.college_id
        )
    ).first()
    if team:
        raise BadRequestException(detail="Team name already exists in this college")

    new_team = Team(
        name=team_in.name,
        problem_statement_id=team_in.problem_statement_id,
        required_skills=team_in.required_skills,
        college_id=user.college_id,
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)

    # Add creator to the team
    user.team_id = new_team.id
    db.add(user)
    db.commit()
    return new_team


def add_user_to_team(db: Session, team_id: uuid.UUID, target_user: User) -> None:
    if target_user.team_id:
        raise BadRequestException(detail="User is already in a team")

    team = db.get(Team, team_id)
    if not team:
        raise NotFoundException(detail="Team not found")

    if len(team.members) >= 6:
        raise BadRequestException(detail="Team is full (Max 6 members)")

    if target_user.college_id != team.college_id:
        raise BadRequestException(
            detail="User must belong to the same college as the team"
        )

    # Check 1 female minimum rule if adding 6th member
    if len(team.members) == 5:
        has_female = any(m.gender.lower() == "female" for m in team.members)
        if not has_female and target_user.gender.lower() != "female":
            raise BadRequestException(
                detail="You need atleast one female member in the team"
            )

    target_user.team_id = team.id
    db.add(target_user)
    db.commit()


def admin_update_team_status(
    db: Session, team_id: uuid.UUID, new_status: TeamStatus, admin: User
) -> Team:
    team = db.get(Team, team_id)
    if not team or team.college_id != admin.college_id:
        raise NotFoundException(detail="Team not found")

    if new_status in [TeamStatus.Shortlisted, TeamStatus.Waitlisted]:
        if len(team.members) != 6:
            raise BadRequestException(
                detail="Team must have exactly 6 members to be shortlisted/waitlisted"
            )

        has_female = any(m.gender.lower() == "female" for m in team.members)
        if not has_female:
            raise BadRequestException(
                detail="Team must have at least 1 female member to be shortlisted/waitlisted"
            )

    # Check limits
    if new_status == TeamStatus.Shortlisted and team.status != TeamStatus.Shortlisted:
        count = len(
            db.exec(
                select(Team).where(
                    Team.college_id == admin.college_id,
                    Team.status == TeamStatus.Shortlisted,
                )
            ).all()
        )
        if count >= 45:
            raise BadRequestException(detail="Maximum 45 teams can be shortlisted")

    elif new_status == TeamStatus.Waitlisted and team.status != TeamStatus.Waitlisted:
        count = len(
            db.exec(
                select(Team).where(
                    Team.college_id == admin.college_id,
                    Team.status == TeamStatus.Waitlisted,
                )
            ).all()
        )
        if count >= 5:
            raise BadRequestException(detail="Maximum 5 teams can be waitlisted")

    team.status = new_status
    db.add(team)
    db.commit()
    db.refresh(team)
    return team
