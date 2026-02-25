from dataclasses import dataclass


@dataclass(frozen=True)
class CurrentUserProfile:
    id: int
    email: str
    full_name: str


@dataclass(frozen=True)
class UserProfile:
    id: int
    email: str
    full_name: str
    is_active: bool
    settings: dict


@dataclass(frozen=True)
class UserUnitAssignment:
    unit_id: int
    unit_name: str
    level: str
