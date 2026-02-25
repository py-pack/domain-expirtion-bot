from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC


class JWTToken:
    def __init__(self, secret_key: str, algorithm: str, access_expire_minutes: int, refresh_expire_days: int):
        self.secret_key: str = secret_key
        self.algorithm: str = algorithm
        self.access_expire_minutes: int = access_expire_minutes
        self.refresh_expire_days: int = refresh_expire_days

    def get_expire_access(self) -> datetime:
        return datetime.now(UTC) + timedelta(minutes=self.access_expire_minutes)

    def get_expire_refresh(self) -> datetime:
        return datetime.now(UTC) + timedelta(days=self.refresh_expire_days)

    def create_access_token(self, data: dict) -> str:
        return self._create_token(data, self.get_expire_access(), "access")

    def create_refresh_token(self, data: dict) -> str:
        return self._create_token(data, self.get_expire_refresh(), "refresh")

    def _create_token(self, data: dict, expire: datetime, token_type: str) -> str:
        to_encode = data.copy()
        to_encode.update({"exp": expire, "type": token_type})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError as e:
            raise ValueError("Invalid token") from e
