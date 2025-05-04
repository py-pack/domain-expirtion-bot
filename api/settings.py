import os
import re
from typing import Optional, ClassVar

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn

PATH_TO_DIR = os.path.dirname(os.path.abspath(__file__))


class LogSettings(BaseSettings):
    path: str = './start.log'
    project_name: str = 'app_monitoring'
    level_log: str = 'DEBUG'
    level_sentry: str = 'ERROR'
    format: str = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
    rotation: str = "5 MB"
    retention: str = "3 days"

    @property
    def path_log(self) -> str:
        local_path = "" if self.path.startswith("/") else PATH_TO_DIR
        return f"{local_path}{self.path}"


class SentrySettings(BaseSettings):
    dsn: str = ''
    trace_rate: float = 0.1
    release: str = "tracker_shadow@0.1.0"
    environment: str = "dev"


class DbSettings(BaseSettings):
    user: str = ''
    password: str = ''
    host: str = ''
    port: int = 5432
    name: str = ''
    echo: bool = True

    @property
    def url(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        )

    @property
    def url_async(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            path=self.name,
        )


class JWTSettings(BaseSettings):
    secret_key: str = ""
    algorithm: str = "HS256"
    access_expire_minutes: int = 15
    refresh_expire_days: int = 7


class GoogleSettings(BaseSettings):
    client_id: str = ""
    client_secret: str = ""
    redirect_uri: str = ""
    scopes: list[str] = ["openid", "email"]


class ApiSettings(BaseSettings):
    env: str = ''
    auth_hash_secret: str = ''
    origins: str = ''

    DEFAULT_LOCALHOST_REGEX: ClassVar[str] = r"http://localhost(:\d+)?"

    # DEFAULT_LDI_REGEX: ClassVar[str] = r"https://(\w+\.)?ldi-apollo\.com"

    @property
    def allow_origin_regex(self) -> str:
        extra = [o.strip().rstrip('/') for o in self.origins.split(',') if o.strip()]
        extra_regexes = [re.escape(origin) for origin in extra]
        patterns = [
                       self.DEFAULT_LOCALHOST_REGEX,
                       # self.DEFAULT_LDI_REGEX,
                       # self.DEFAULT_LDI_ORG_REGEX
                   ] + extra_regexes
        return r"^(" + "|".join(patterns) + r")$"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP__",
        env_ignore_empty=True,
        extra="ignore",
    )

    x_token: Optional[str] = None
    api: ApiSettings = ApiSettings()

    db: DbSettings = DbSettings()

    jwt: JWTSettings = JWTSettings()
    google: GoogleSettings = GoogleSettings()

    # Log settings
    log: LogSettings = LogSettings()
    sentry: SentrySettings = SentrySettings()


settings = Settings()

print(settings)