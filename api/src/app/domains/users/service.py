from typing import Any, Optional

from sqlalchemy.orm import Session

from app.domains.auth.models import User
from app.domains.auth.service import decode_jwt, hash_password, verify_password

from .models import CurrentUserProfile, UserProfile
from .repository import (
    create_user,
    delete_user,
    get_user_by_email,
    get_user_by_id,
    list_users,
    save_user,
)


class UsersDomainError(Exception):
    pass


class InvalidAccessTokenError(UsersDomainError):
    pass


class UserNotFoundError(UsersDomainError):
    pass


class InvalidCurrentPasswordError(UsersDomainError):
    pass


class UserAlreadyExistsError(UsersDomainError):
    pass


def _extract_user_id_from_access_token(access_token: str) -> int:
    try:
        payload = decode_jwt(access_token)
    except Exception as error:
        raise InvalidAccessTokenError("Invalid token") from error

    if payload.get("type") != "access":
        raise InvalidAccessTokenError("Wrong token type")

    user_id_raw = payload.get("sub")
    if not isinstance(user_id_raw, str):
        raise InvalidAccessTokenError("Invalid token subject")

    try:
        return int(user_id_raw)
    except ValueError as error:
        raise InvalidAccessTokenError("Invalid token subject") from error


def _build_current_user_profile(user: User) -> CurrentUserProfile:
    return CurrentUserProfile(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
    )


def _build_user_profile(user: User) -> UserProfile:
    return UserProfile(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        is_active=user.is_active,
        settings=user.settings,
    )


def get_current_user_profile(db: Session, access_token: str) -> CurrentUserProfile:
    user_id = _extract_user_id_from_access_token(access_token)
    user = get_user_by_id(db, user_id)

    if not user:
        raise UserNotFoundError("User not found")

    return _build_current_user_profile(user)


def update_current_user_profile(
    db: Session,
    access_token: str,
    full_name: str,
    current_password: Optional[str] = None,
    new_password: Optional[str] = None,
) -> CurrentUserProfile:
    user_id = _extract_user_id_from_access_token(access_token)
    user = get_user_by_id(db, user_id)

    if not user:
        raise UserNotFoundError("User not found")

    normalized_full_name = full_name.strip()
    user.full_name = normalized_full_name

    if new_password:
        if not current_password:
            raise InvalidCurrentPasswordError("Current password is required")

        if not verify_password(current_password, user.hashed_password):
            raise InvalidCurrentPasswordError("Current password is incorrect")

        user.hashed_password = hash_password(new_password)

    updated_user = save_user(db, user)
    return _build_current_user_profile(updated_user)


def list_system_users(db: Session) -> list[UserProfile]:
    users = list_users(db)
    return [_build_user_profile(user) for user in users]


def get_system_user(db: Session, user_id: int) -> UserProfile:
    user = get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundError("User not found")

    return _build_user_profile(user)


def create_system_user(
    db: Session,
    email: str,
    full_name: str,
    password: str,
    is_active: bool = True,
    settings: Optional[dict[str, Any]] = None,
) -> UserProfile:
    normalized_email = email.strip().lower()
    normalized_full_name = full_name.strip()

    if get_user_by_email(db, normalized_email):
        raise UserAlreadyExistsError("User already exists")

    user = User(
        email=normalized_email,
        full_name=normalized_full_name,
        hashed_password=hash_password(password),
        is_active=is_active,
        settings=settings or {},
    )

    created_user = create_user(db, user)
    return _build_user_profile(created_user)


def update_system_user(
    db: Session,
    user_id: int,
    email: Optional[str] = None,
    full_name: Optional[str] = None,
    password: Optional[str] = None,
    is_active: Optional[bool] = None,
    settings: Optional[dict[str, Any]] = None,
) -> UserProfile:
    user = get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundError("User not found")

    if email is not None:
        normalized_email = email.strip().lower()
        existing_user = get_user_by_email(db, normalized_email)
        if existing_user and existing_user.id != user.id:
            raise UserAlreadyExistsError("User already exists")
        user.email = normalized_email

    if full_name is not None:
        user.full_name = full_name.strip()

    if password is not None:
        user.hashed_password = hash_password(password)

    if is_active is not None:
        user.is_active = is_active

    if settings is not None:
        user.settings = settings

    updated_user = save_user(db, user)
    return _build_user_profile(updated_user)


def delete_system_user(db: Session, user_id: int) -> None:
    user = get_user_by_id(db, user_id)
    if not user:
        raise UserNotFoundError("User not found")

    delete_user(db, user)
