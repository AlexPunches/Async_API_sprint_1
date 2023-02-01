"""Генератор фейковых данных.

При seed(0), юзеров 1К, фильмов 1К
получаем 111_168_000 штук.
"""
import datetime
import time
from dataclasses import dataclass
from typing import Generator, List
from uuid import UUID

from faker import Faker

from config import logger

fake = Faker()
Faker.seed(0)


@dataclass
class User:
    """Дата-класс Пользователь."""

    id: UUID


@dataclass
class Film:
    """Дата-класс Фильм."""

    id: UUID
    duration: int


@dataclass
class Point:
    """Дата-класс Момент фильма."""

    user_id: UUID
    film_id: UUID
    value: int
    created_at: int


def create_users(count: int) -> List[User]:
    """Создать список юзеров."""
    return [User(id=fake.uuid4()) for _ in range(count)]


def create_films(count: int) -> List[Film]:
    """Создать список фильмов."""
    return [Film(
        id=fake.uuid4(),
        duration=fake.random_int(min=20, max=200),
        ) for _ in range(count)]


def generate_points(users_count: int, films_count: int) -> Generator:
    """Сгенерировать события.

    Получается, что каждый юзер посмотрит каждый фильм от начала до конца
    без перерыва и перемоток. Время начала просмотра рандомное.
    """
    duration = 0
    users = create_users(users_count)
    films = create_films(films_count)

    for user in users:
        start_user = datetime.datetime(2022, 1, 1, 0, 0, 1)
        start_film = int(time.mktime(start_user.timetuple()))
        for film in films:
            for minute in range(film.duration):
                duration += 1
                yield Point(
                    user_id=user.id,
                    film_id=film.id,
                    value=minute,
                    created_at=start_film + ((minute + 1) * 60),
                    )
            start_film += film.duration

    logger.info(f'готово points: {duration}')
