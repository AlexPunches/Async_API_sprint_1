"""Модели активностей."""

from uuid import UUID

import orjson
from pydantic import BaseModel

from src.utils import orjson_dumps


class SpawnPointModel(BaseModel):
    """Модель момента фильма, во время просмотра пользователем."""

    user_id: UUID | None = None
    film_id: str
    time: int

    class Config: # noqa
        json_loads = orjson.loads
        json_dumps = orjson_dumps
