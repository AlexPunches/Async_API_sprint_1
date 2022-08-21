"""
/api/v1/persons/search/
/api/v1/persons/<uuid:UUID>/
/api/v1/persons/<uuid:UUID>/film/
"""
from http import HTTPStatus
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field
from services.film import FilmService, get_film_service

from fastapi import APIRouter, Depends, HTTPException

router = APIRouter()


class FilmShort(BaseModel):
    uuid: str
    title: str
    imdb_rating: Optional[float]


class Person(BaseModel):
    id: UUID = Field(..., alias='uuid')
    name: str = Field(..., alias='full_name')
    role: str  # TODO может быть список все таки тут?
    film_ids: Optional[list[UUID]]

    class Config:
        allow_population_by_field_name = True
