from http import HTTPStatus

import pytest

from functional.settings import test_settings

pytestmark = pytest.mark.asyncio


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        ({'query': 'Question set'}, {'status': HTTPStatus.OK, 'length': 1}),
        ({'query': 'Glass'}, {'status': HTTPStatus.OK, 'length': 2}),
        ({'query': 'AAABBBCCC'}, {'status': HTTPStatus.OK, 'length': 0}),
    ]
)
async def test_search(
          es_write_data,
          es_determination_data,
          query_data,
          expected_answer,
          aiohttp_get,
):
    """Поиск по фильмам работает корректно."""
    await es_write_data(
        data=es_determination_data['films'],
        es_index=test_settings.es_indexes['movies']
    )

    headers = {'X-Not-Cache': 'True'}
    url = test_settings.service_url + '/api/v1/films/search/'
    response = await aiohttp_get(url=url, headers=headers, params=query_data)

    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']


@pytest.mark.parametrize(
    'query_data, expected_answer',
    [
        ({'query': 'wikipedia amazon', 'page[size]': '3', 'page[number]': '1'},
         {'status': HTTPStatus.OK, 'length': 3}),
        ({'query': 'wikipedia amazon', 'page[size]': '3', 'page[number]': '2'},
         {'status': HTTPStatus.OK, 'length': 2}),
    ]
)
async def test_search_paginate(
          es_write_data,
          es_determination_data,
          query_data,
          expected_answer,
          aiohttp_get,
):
    """Пагинация на поиске по фильмам работает корректно."""
    await es_write_data(
        data=es_determination_data['films'],
        es_index=test_settings.es_indexes['movies']
    )

    headers = {'X-Not-Cache': 'True'}
    url = test_settings.service_url + '/api/v1/films/search/'
    response = await aiohttp_get(url=url, headers=headers, params=query_data)

    assert response['status'] == expected_answer['status']
    assert len(response['body']) == expected_answer['length']
