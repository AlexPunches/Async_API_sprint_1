"""Фикстуры клиентов."""
from typing import Generator

import aioredis
import psycopg2
import pytest
from psycopg2.extras import DictCursor
from redis.client import Redis

from functional.settings import test_settings
from functional.utils.http_client import HttpClient
from functional.utils.user_action import UserActions


# Фикстура еще не проверялась в действии
@pytest.fixture(scope='session')
def redis_client() -> Generator[None, Redis, None]:
    """Получить клиент Редиса перед сессией и закрыть его в конце сессии."""
    _client = aioredis.create_redis_pool(
        (test_settings.redis_host, test_settings.redis_port),
        minsize=10,
        maxsize=20,
    )
    yield _client
    _client.close()


@pytest.fixture(scope='session')
def pg_conn():
    """Подключиться к БД."""
    with psycopg2.connect(
                          dbname=test_settings.pg_settings.db_name,
                          user=test_settings.pg_settings.username,
                          password=test_settings.pg_settings.password,
                          host=test_settings.pg_settings.host,
                          port=test_settings.pg_settings.port,
                          cursor_factory=DictCursor,
                          ) as pg_conn:
        yield pg_conn


@pytest.fixture(scope='session')
def pg_cursor(pg_conn):
    """Получить курсор."""
    pg_cursor = pg_conn.cursor()
    yield pg_cursor


@pytest.fixture(scope='session')
def user_action():
    """Получить класс-эмулятор действий пользователя."""
    return UserActions()


@pytest.fixture(scope='session')
def http_client():
    """HTTP-клиент для тестов."""
    return HttpClient()
