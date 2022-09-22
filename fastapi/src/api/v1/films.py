"""
/api/v1/films?sort=-imdb_rating
/api/v1/films?sort=-imdb_rating&filter[genre]=<comedy-uuid>
/api/v1/films/search/
✓   /api/v1/films/<uuid:UUID>/
/api/v1/films?... # покажем фильмы того же жанра.
/api/v1/films...  # Популярные фильмы в жанре.
"""

from http import HTTPStatus

from api.v1 import ElasticPaginateSort
from api.v1.shemes.film import Film, FilmShort
from api.v1.shemes.transform_schemes import (es_film_to_film_scheme,
                                             es_film_to_film_short_scheme)
from elasticsearch import BadRequestError
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from services.film import FilmService, get_film_service

from fastapi import Depends, HTTPException, Query

router = InferringRouter()


@cbv(router)
class FilmCBV:
    film_service: FilmService = Depends(get_film_service)
    params: ElasticPaginateSort = Depends()

    @router.get('/')
    async def film_list(
        self,
        filter_genre: str | None = Query(default=None, alias='filter[genre]'),
    ) -> list[Film]:
        films = await self.film_service.get_all()
        return [es_film_to_film_scheme(film) for film in films]

    @router.get('/search')
    async def film_search(
        self,
        query: str | None = Query(default=None)
    ) -> list[FilmShort]:
        try:
            films = await self.film_service.search(
                page_size=self.params.page.size,
                page_number=self.params.page.number,
                sort=self.params.sort,
                query=query,
            )
        except BadRequestError as e:
            raise HTTPException(status_code=e.status_code,
                                detail=f'Bad Request. {e.error}')
        return [es_film_to_film_short_scheme(film) for film in films]


@router.get('/{film_id}', response_model=Film)
async def film_details(
          film_id: str,
          film_service: FilmService = Depends(get_film_service),
) -> Film:
    if film := await film_service.get_by_id(film_id):
        return es_film_to_film_scheme(film)
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND,
                        detail='film not found')
