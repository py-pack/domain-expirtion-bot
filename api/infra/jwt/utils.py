from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC


class JWTToken:
    def __init__(self, secret_key: str, algorithm: str, access_expire_minutes: int, refresh_expire_days: int):
        self.secret_key: str = secret_key
        self.algorithm: str = algorithm
        self.access_expire_minutes: int = access_expire_minutes
        self.refresh_expire_days: int = refresh_expire_days

    def create_access_token(self, data: dict) -> str:
        return self._create_token(data, timedelta(minutes=self.access_expire_minutes), "access")

    def create_refresh_token(self, data: dict) -> str:
        return self._create_token(data, timedelta(days=self.refresh_expire_days), "refresh")

    def _create_token(self, data: dict, expire_delta: timedelta, token_type: str) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + expire_delta
        to_encode.update({"exp": expire, "type": token_type})
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)

    def decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        except JWTError as e:
            raise ValueError("Invalid token") from e
