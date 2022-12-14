"""Бенчмаркинг кликхауса.

Тачка:
Платформа Intel Ice Lake
Гарантированная доля vCPU 100%
vCPU 4
RAM 16 ГБ
Объём дискового пространства 100 ГБ
Прерываемая да

Все 3 шарда в докерах на одной машине.
"""
import random
from typing import Generator

import more_itertools
from clickhouse_driver import Client
from generator_fakes import generate_points
from timer import timed

CHUNK_SIZE: int = 10 ** 4
print(f'CHUNK_SIZE: {CHUNK_SIZE}')


@timed
def load_data(data: Generator):
    """Загрузить данные в кликхаус.

    Каждая пачка на случайный шард.
    """
    clients = (
        Client(host='localhost', port='9000'),
        Client(host='localhost', port='9003'),
        Client(host='localhost', port='9005'),
    )
    for points in more_itertools.ichunked(data, CHUNK_SIZE):
        client = random.choice(clients)
        client.execute(
             'INSERT INTO shard.test (user_id, film_id, event_time, spawn_point) VALUES',  # noqa
             ((point.user_id, point.film_id, point.created_at, point.value) for point in points),  # noqa
         )


def run() -> None:
    data = generate_points(users_count=1000, films_count=1000)
    load_data(data)


if __name__ == "__main__":
    run()
