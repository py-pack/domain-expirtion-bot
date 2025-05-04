from typing import cast, Type
from passlib.hash import bcrypt_sha256
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from infra.jwt import create_access_token, create_refresh_token
from .models import User
from .repository import get_user_by_email, create_user


def _verify_password(password: str, hashed: str) -> bool:
    return bcrypt_sha256.verify(password, hashed)


def _hash_password(password: str) -> str:
    return bcrypt_sha256.hash(password)


def _generate_tokens(user: Type[User]):
    payload = {"sub": str(user.id), "email": user.email}
    return {
        "access_token": create_access_token(payload),
        "refresh_token": create_refresh_token(payload),
        "token_type": "bearer",
    }


def authenticate_user(db: Session, email: str, password: str) -> Type[User] | None:
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")

    hashed = cast(str, user.hashed_password)
    if not _verify_password(password, hashed):
        raise HTTPException(status_code=403, detail="Invalid credentials")
    return user


def login_for_tokens(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    return _generate_tokens(user)


def login_user_by_email(db: Session, email: str):
    user = get_user_by_email(db, email)
    if not user:
        raise HTTPException(status_code=403, detail="Invalid credentials")
    return _generate_tokens(user)


def add_user(db: Session, email: str, password: str) -> User:
    if get_user_by_email(db, email):
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = _hash_password(password)
    user = User(email=email, hashed_password=hashed_password)
    return create_user(db, user)
