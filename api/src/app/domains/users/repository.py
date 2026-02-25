from collections.abc import Sequence
from typing import Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domains.auth.models import User
from app.domains.units.models import Unit, UnitResponsible


def list_users(db: Session) -> list[User]:
    return db.query(User).order_by(User.id.asc()).all()


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def save_user(db: Session, user: User) -> User:
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user: User) -> None:
    db.delete(user)
    db.commit()


def list_user_unit_assignments(db: Session, user_id: int) -> list[tuple[int, str, object]]:
    statement = (
        select(Unit.id, Unit.name, UnitResponsible.level)
        .join(UnitResponsible, UnitResponsible.unit_id == Unit.id)
        .where(UnitResponsible.user_id == user_id)
        .order_by(Unit.id.asc())
    )
    rows = db.execute(statement).all()
    return [(int(row[0]), str(row[1]), row[2]) for row in rows]


def list_units_by_ids(db: Session, unit_ids: Sequence[int]) -> list[Unit]:
    if not unit_ids:
        return []

    statement = select(Unit).where(Unit.id.in_(list(unit_ids))).order_by(Unit.id.asc())
    return list(db.scalars(statement).all())


def replace_user_unit_assignments(
    db: Session,
    user_id: int,
    assignments: Sequence[tuple[int, object]],
) -> None:
    db.query(UnitResponsible).filter(UnitResponsible.user_id == user_id).delete()

    for unit_id, level in assignments:
        db.add(UnitResponsible(unit_id=unit_id, user_id=user_id, level=level))

    db.commit()
