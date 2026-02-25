from sqlalchemy.orm import Session

from app.domains.auth.models import User

from .models import (
    Unit,
    UnitDetails,
    UnitListItem,
    UnitResponsibleLevel,
    UnitResponsibleUser,
)
from .repository import (
    create_unit,
    delete_unit,
    get_unit_by_id,
    get_unit_by_name,
    list_unit_responsibles,
    list_units,
    list_users_by_ids,
    replace_unit_responsibles,
    save_unit,
)


class UnitsDomainError(Exception):
    pass


class UnitNotFoundError(UnitsDomainError):
    pass


class UnitAlreadyExistsError(UnitsDomainError):
    pass


class UnitResponsibleUsersNotFoundError(UnitsDomainError):
    def __init__(self, missing_user_ids: list[int]):
        self.missing_user_ids = missing_user_ids
        super().__init__(f"Users not found: {', '.join(str(user_id) for user_id in missing_user_ids)}")


def _normalize_unit_name(name: str) -> str:
    return name.strip()


def _build_unit_details(unit: Unit) -> UnitDetails:
    return UnitDetails(id=unit.id, name=unit.name)


def _build_unit_list_item(unit: Unit, responsibles_count: int) -> UnitListItem:
    return UnitListItem(id=unit.id, name=unit.name, responsibles_count=responsibles_count)


def _build_responsible_user(user: User, level: str | UnitResponsibleLevel) -> UnitResponsibleUser:
    return UnitResponsibleUser(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        level=level.value if isinstance(level, UnitResponsibleLevel) else level,
    )


def _normalize_level(level: str) -> str:
    normalized_level = level.strip()
    if not normalized_level:
        raise ValueError("Responsible level is required")

    try:
        return UnitResponsibleLevel(normalized_level).value
    except ValueError as error:
        raise ValueError("Responsible level must be one of: View, Edit, Full") from error


def list_system_units(db: Session) -> list[UnitListItem]:
    rows = list_units(db)
    return [_build_unit_list_item(unit, count) for unit, count in rows]


def get_system_unit(db: Session, unit_id: int) -> UnitDetails:
    unit = get_unit_by_id(db, unit_id)
    if not unit:
        raise UnitNotFoundError("Unit not found")

    return _build_unit_details(unit)


def create_system_unit(db: Session, name: str) -> UnitDetails:
    normalized_name = _normalize_unit_name(name)

    if not normalized_name:
        raise ValueError("Unit name is required")

    if get_unit_by_name(db, normalized_name):
        raise UnitAlreadyExistsError("Unit already exists")

    unit = Unit(name=normalized_name)
    created_unit = create_unit(db, unit)
    return _build_unit_details(created_unit)


def update_system_unit(db: Session, unit_id: int, name: str | None = None) -> UnitDetails:
    unit = get_unit_by_id(db, unit_id)
    if not unit:
        raise UnitNotFoundError("Unit not found")

    if name is not None:
        normalized_name = _normalize_unit_name(name)
        if not normalized_name:
            raise ValueError("Unit name is required")

        existing_unit = get_unit_by_name(db, normalized_name)
        if existing_unit and existing_unit.id != unit.id:
            raise UnitAlreadyExistsError("Unit already exists")

        unit.name = normalized_name

    updated_unit = save_unit(db, unit)
    return _build_unit_details(updated_unit)


def delete_system_unit(db: Session, unit_id: int) -> None:
    unit = get_unit_by_id(db, unit_id)
    if not unit:
        raise UnitNotFoundError("Unit not found")

    delete_unit(db, unit)


def list_system_unit_responsibles(db: Session, unit_id: int) -> list[UnitResponsibleUser]:
    if not get_unit_by_id(db, unit_id):
        raise UnitNotFoundError("Unit not found")

    rows = list_unit_responsibles(db, unit_id)
    return [_build_responsible_user(user, level) for user, level in rows]


def replace_system_unit_responsibles(
    db: Session,
    unit_id: int,
    assignments: list[dict[str, object]],
) -> list[UnitResponsibleUser]:
    if not get_unit_by_id(db, unit_id):
        raise UnitNotFoundError("Unit not found")

    normalized_assignments: list[tuple[int, str]] = []
    unique_user_ids: list[int] = []
    seen_user_ids: set[int] = set()

    for assignment in assignments:
        user_id_raw = assignment.get("user_id")
        level_raw = assignment.get("level")
        if not isinstance(user_id_raw, int) or user_id_raw <= 0:
            raise ValueError("Invalid responsible user_id")
        if not isinstance(level_raw, str):
            raise ValueError("Invalid responsible level")

        if user_id_raw in seen_user_ids:
            raise ValueError("Responsible users must be unique")

        seen_user_ids.add(user_id_raw)
        unique_user_ids.append(user_id_raw)
        normalized_assignments.append((user_id_raw, _normalize_level(level_raw)))

    users = list_users_by_ids(db, unique_user_ids)
    found_user_ids = {user.id for user in users}
    missing_user_ids = [user_id for user_id in unique_user_ids if user_id not in found_user_ids]

    if missing_user_ids:
        raise UnitResponsibleUsersNotFoundError(missing_user_ids)

    replace_unit_responsibles(db, unit_id, normalized_assignments)
    updated_rows = list_unit_responsibles(db, unit_id)
    return [_build_responsible_user(user, level) for user, level in updated_rows]
