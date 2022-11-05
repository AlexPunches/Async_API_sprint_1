"""Тесты Пользователя."""
from http import HTTPStatus

import pytest
import requests
from functional.settings import test_settings
from functional.testdata.faker_data import get_faker_data

faker_data = get_faker_data()


# @pytest.mark.skip(reason='')
@pytest.mark.parametrize('user', [faker_data.users[0]])
def test_user_detail(db_insert_fake_data, pg_cursor, user):
    """Детальная информация о пользователе корректная."""
    url = test_settings.service_url
    url += '/api/v1/users/{user_id}/'.format(user_id=user.id)
    response = requests.get(url)

    r_user = response.json()

    assert response.status_code == HTTPStatus.OK
    assert r_user.get('email') == user.email
    assert r_user.get('login') == user.login


# @pytest.mark.skip(reason='')
@pytest.mark.parametrize('user', [faker_data.users[10]])
def test_user_after_edit_response(db_insert_fake_data, pg_cursor, user):
    """После редактирования получаем корректный ответ с новыми данными."""
    new_login = 'aaaaaa'
    new_email = 'aaa@aaa.aa'
    headers = {'accept': 'application/json'}
    url = test_settings.service_url
    url += '/api/v1/users/{user_id}/'.format(user_id=user.id)
    payload = {'email': new_email, 'login': new_login}

    response = requests.patch(url, json=payload, headers=headers)
    r_user = response.json()

    assert response.status_code == HTTPStatus.OK
    assert r_user.get('login') == new_login
    assert r_user.get('email') == new_email


# @pytest.mark.skip(reason='')
@pytest.mark.parametrize('user', [faker_data.users[10]])
def test_user_edit(db_insert_fake_data, pg_cursor, user):
    """Данные ползователя редактируются корректно."""
    new_login = 'aaaaaa'
    new_email = 'aaa@aaa.aa'
    headers = {'accept': 'application/json'}
    url = test_settings.service_url
    url += '/api/v1/users/{user_id}/'.format(user_id=user.id)
    payload = {'email': new_email, 'login': new_login}

    response = requests.patch(url, json=payload, headers=headers)
    pg_stmt = f'SELECT * FROM {test_settings.users_tablename} '
    pg_stmt += f"WHERE id = '{faker_data.users[10].id}';"
    pg_cursor.execute(pg_stmt)

    count_obj = pg_cursor.fetchall()

    assert response.status_code == HTTPStatus.OK
    assert len(count_obj) == 1
    assert count_obj[0]['email'] == new_email
    assert count_obj[0]['login'] == new_login
