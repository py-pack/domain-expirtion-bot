import sys
import time
from loguru import logger as loguru_logger
from sentry_sdk import capture_exception
from app.core.config import settings

# Remove all existing handlers to prevent duplicate logs
loguru_logger.remove()

# 🔧 Конфігурація loguru
loguru_logger.configure(extra={"project": settings.log.project_name})

# Лог-файл
loguru_logger.add(
    settings.log.path_log,
    serialize=True,
    format=settings.log.format,
    rotation=settings.log.rotation,
    retention=settings.log.retention,
)

# Вивід у консоль (для docker logs)
loguru_logger.add(sys.stdout, level=settings.log.level_log)


# Log-decorator для функцій
def log_task(func):
    def wrapper(*args, **kwargs):
        task_name = func.__name__
        loguru_logger.info(f"Task '{task_name}' started with args: {args}, kwargs: {kwargs}")
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            end_time = time.time()
            elapsed_time = end_time - start_time
            loguru_logger.info(f"Task '{task_name}' completed with result: {result}")
            loguru_logger.info(f"Task '{task_name}' took {elapsed_time:.2f} seconds to complete")
            return result
        except Exception as e:
            loguru_logger.error(f"Task '{task_name}' exceed with exception: {e}")
            raise e

    return wrapper


# 🎯 Sentry-хендлер для loguru
class SentryHandler:
    def __call__(self, record):
        if record["level"].name in ("ERROR", "CRITICAL"):
            ex = record["exception"]
            if ex:
                capture_exception(ex)
            else:
                capture_exception(Exception(record["message"]))


loguru_logger.add(SentryHandler(), level=settings.log.level_sentry)


# 🧱 Сервіс-обгортка
class LoggerService:
    def __init__(self):
        self.logger = loguru_logger

    def debug(self, msg, *args, **kwargs):
        self.logger.opt(depth=1).debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.opt(depth=1).info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.opt(depth=1).warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.opt(depth=1).error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.opt(depth=1).exception(msg, *args, **kwargs)

    def capture_exception(self, exception: Exception):
        capture_exception(exception)
        self.logger.opt(depth=1).exception(exception)
