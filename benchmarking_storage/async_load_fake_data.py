import asyncio
from asyncio import sleep
from typing import Generator

import more_itertools
from aiochclient import ChClient
from aiohttp import ClientSession
from generator_fakes import generate_points

CHUNK_SIZE: int = 10 ** 5
print(f'CHUNK_SIZE: {CHUNK_SIZE}')


async def load_data(client: ChClient, data: Generator):
    for points in more_itertools.ichunked(data, CHUNK_SIZE):
        await client.execute(
             'INSERT INTO shard.test (user_id, film_id, event_time, spawn_point) VALUES',
             *[(point.user_id, point.film_id, point.created_at, point.value) for point in points]
        )


async def run() -> None:
    data = generate_points(users_count=10, films_count=10)
    async with ClientSession() as s:
        # load_data_1 = asyncio.create_task(load_data(client=ChClient(s, url='http://localhost:8123'), data=data))
        # load_data_2 = asyncio.create_task(load_data(client=ChClient(s, url='http://localhost:28123'), data=data))
        # load_data_3 = asyncio.create_task(load_data(client=ChClient(s, url='http://localhost:38123'), data=data))
        #
        # await load_data_1
        # await load_data_2
        # await load_data_3
        await sleep(2)

if __name__ == "__main__":
    asyncio.run(run())
