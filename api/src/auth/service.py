from uuid import UUID
from typing import cast, Optional
from datetime import datetime
from passlib.hash import bcrypt_sha256

from infra.jwt import JWTToken
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, delete, or_

from .models import User, RefreshToken
from .repository import get_user_by_email, create_user

from settings import settings

jwt_generator = JWTToken(
    settings.jwt.secret_key,
    settings.jwt.algorithm,
    settings.jwt.access_expire_minutes,
    settings.jwt.refresh_expire_days
)


def _verify_password(password: str, hashed: str) -> bool:
    return bcrypt_sha256.verify(password, hashed)


def _hash_password(password: str) -> str:
    return bcrypt_sha256.hash(password)


def _generate_tokens(user: User):
    payload = {"sub": str(user.id), "email": user.email}

    return {
        "access_token": jwt_generator.create_access_token(payload),
        "refresh_token": jwt_generator.create_refresh_token(payload),
        "token_type": "bearer",
    }


def _authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    hashed = cast(str, user.hashed_password)
    if not _verify_password(password, hashed):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    return user


def login_for_tokens(db: Session, email: str, password: str, session_id: UUID, user_agent: str):
    user = _authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    result = _generate_tokens(user)
    create_token(db, user.id, result.get('refresh_token'), jwt_generator.get_expire_refresh(), session_id, user_agent)
    db.commit()

    return result


def login_user_by_email(db: Session, email: str, session_id: UUID, user_agent: str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    result = _generate_tokens(user)
    create_token(db, user.id, result.get('refresh_token'), jwt_generator.get_expire_refresh(), session_id, user_agent)
    db.commit()

    return result


def add_user(db: Session, email: str, password: str) -> User:
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = _hash_password(password)
    user = User(email=email, hashed_password=hashed_password)
    return create_user(db, user)


def decode_jwt(token: str) -> dict:
    try:
        return jwt_generator.decode_token(token)
    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))


def get_token(db: Session, token: str):
    stmt = select(RefreshToken).where(RefreshToken.token == token)
    result = db.execute(stmt)
    return result.scalar_one_or_none()


def delete_token(db: Session, token: Optional[str] = None, session_id: Optional[UUID] = None):
    stmt = delete(RefreshToken)
    conditions = []
    if token is not None:
        conditions.append(RefreshToken.token == token)
    if session_id is not None:
        conditions.append(RefreshToken.session_id == str(session_id))
    if conditions:
        stmt = stmt.where(or_(*conditions))
        db.execute(stmt)
        db.commit()


def create_token(
        db: Session,
        user_id: int,
        token: str,
        expires_at: datetime,
        session_id: UUID,
        user_agent: Optional[str] = None
):
    delete_token(db, token=token, session_id=session_id)

    new_token = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at,
        session_id=session_id,
        user_agent=user_agent,
    )
    db.add(new_token)
    db.commit()

    return new_token
