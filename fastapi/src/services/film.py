from functools import lru_cache

from db.elastic import get_elastic
from elasticsearch import AsyncElasticsearch
from models.film import Film
from services import BaseElasticService

from fastapi import Depends


class FilmService(BaseElasticService):
    pass


@lru_cache()
def get_film_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(elastic, es_index='movies', es_model=Film)
