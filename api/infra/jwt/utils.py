from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC
from settings import settings


def _create_token(data: dict, expire_delta: timedelta, token_type: str) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + expire_delta
    to_encode.update({"exp": expire, "type": token_type})
    return jwt.encode(to_encode, settings.jwt.secret_key, algorithm=settings.jwt.algorithm)


def create_access_token(data: dict) -> str:
    return _create_token(data, timedelta(minutes=settings.jwt.access_expire_minutes), "access")


def create_refresh_token(data: dict) -> str:
    return _create_token(data, timedelta(days=settings.jwt.refresh_expire_days), "refresh")


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm])
    except JWTError as e:
        raise ValueError("Invalid token") from e
