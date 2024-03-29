import logging
from functools import lru_cache
from logging import config as logging_config

from pydantic import BaseSettings, Field

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class AmqpConect(BaseSettings):
    notifications_queue_user: str
    notifications_queue_password: str
    notifications_queue_host: str = '51.250.2.205'
    notifications_queue_port: str = '5672'

    def get_conn_str(self) -> str:
        """Получить троку подключения к Реббиту."""
        return str(
            f'amqp://{self.notifications_queue_user}'
            f':{self.notifications_queue_password}@'
            f'{self.notifications_queue_host}:{self.notifications_queue_port}/'
        )


class WorkerSettings(BaseSettings):
    project_name: str = Field('Movies', env='project_name')
    queue_prefetch_count: int = 1
    queue_name: str = 'notifications'
    exchanger_name: str = 'notifications_exchanger'
    retry_queue_name: str = 'retry_notifications'
    retry_exchanger_name: str = 'notifications_retry_exchanger'
    ttl_for_retry: int = 600000
    queue_conn_str: str = AmqpConect().get_conn_str()
    mq_timeout: int = 10
    def_priority: int = 5
    max_priority: int = 10
    def_timezone: str = 'Europe/Moscow'
    night_start_hour: int = Field(22, ge=0, le=24)
    night_stop_hour: int = Field(8, ge=0, le=24)
    smtp_host: str = 'localhost'
    smtp_port: str = '1025'
    smtp_from: str = 'email@email.email'
    smtp_username: str = 'root'
    smtp_password: str = 'root'


@lru_cache()
def get_settings() -> WorkerSettings:
    """Получить синглтон конфигов."""
    return WorkerSettings()


config = get_settings()
logger = logging.getLogger(config.project_name)
