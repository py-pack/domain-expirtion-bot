from collections.abc import Sequence

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.domains.auth.models import User

from .models import Unit, UnitResponsible


def list_units(db: Session) -> list[tuple[Unit, int]]:
    statement = (
        select(Unit, func.count(UnitResponsible.id).label("responsibles_count"))
        .outerjoin(UnitResponsible, UnitResponsible.unit_id == Unit.id)
        .group_by(Unit.id)
        .order_by(Unit.id.asc())
    )
    rows = db.execute(statement).all()
    return [(row[0], int(row[1])) for row in rows]


def get_unit_by_id(db: Session, unit_id: int) -> Unit | None:
    return db.query(Unit).filter(Unit.id == unit_id).first()


def get_unit_by_name(db: Session, name: str) -> Unit | None:
    return db.query(Unit).filter(func.lower(Unit.name) == func.lower(name)).first()


def create_unit(db: Session, unit: Unit) -> Unit:
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


def save_unit(db: Session, unit: Unit) -> Unit:
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit


def delete_unit(db: Session, unit: Unit) -> None:
    db.delete(unit)
    db.commit()


def list_unit_responsibles(db: Session, unit_id: int) -> list[tuple[User, object]]:
    statement = (
        select(User, UnitResponsible.level)
        .join(UnitResponsible, UnitResponsible.user_id == User.id)
        .where(UnitResponsible.unit_id == unit_id)
        .order_by(User.id.asc())
    )
    rows = db.execute(statement).all()
    return [(row[0], row[1]) for row in rows]


def list_users_by_ids(db: Session, user_ids: Sequence[int]) -> list[User]:
    if not user_ids:
        return []

    statement = select(User).where(User.id.in_(list(user_ids))).order_by(User.id.asc())
    return list(db.scalars(statement).all())


def replace_unit_responsibles(
    db: Session,
    unit_id: int,
    assignments: Sequence[tuple[int, str]],
) -> None:
    db.query(UnitResponsible).filter(UnitResponsible.unit_id == unit_id).delete()

    for user_id, level in assignments:
        db.add(UnitResponsible(unit_id=unit_id, user_id=user_id, level=level))

    db.commit()
