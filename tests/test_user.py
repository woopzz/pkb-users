import uuid

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.security import parse_token
from app.models import UserPublic
from app.service import create_token

from .utils import create_user

URL_USERS = f'{settings.API_V1_STR}/users'
URL_TOKEN = f'{settings.API_V1_STR}/access-token'


@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    name = 'some unique name'
    password = 'long-enough-password'

    response = await client.post(URL_USERS, json={'name': name, 'password': password})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert uuid.UUID(data['id'])
    assert data['name'] == name


@pytest.mark.asyncio
async def test_create_user_with_not_unique_name(session: AsyncSession, client: AsyncClient):
    name = 'not unique name'
    password = 'user password'
    await create_user(session, name='not unique name')

    response = await client.post(URL_USERS, json={'name': name, 'password': password})
    assert response.status_code == 400
    assert response.json() == {'detail': 'This username is already taken.'}


@pytest.mark.asyncio
async def test_create_access_token(session: AsyncSession, client: AsyncClient):
    name = 'user name'
    password = 'user password'
    user = await create_user(session, name=name, password=password)

    response = await client.post(URL_TOKEN, json={'name': name, 'password': password})
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 2
    assert data['token_type'] == 'bearer'

    token = data['access_token']
    ok, user_id = parse_token(token)
    assert ok
    assert str(user.id) == user_id


@pytest.mark.asyncio
async def test_create_access_token_for_missing_user(client: AsyncClient):
    response = await client.post(URL_TOKEN, json={'name': 'random', 'password': 'random random'})
    assert response.status_code == 404
    assert response.json() == {'detail': 'User not found.'}


@pytest.mark.asyncio
async def test_read_my_user(session: AsyncSession, client: AsyncClient):
    user = await create_user(session)
    token = create_token(str(user.id))

    response = await client.get(
        URL_USERS + '/me',
        headers={'Authorization': 'Bearer ' + token.access_token},
    )
    assert response.status_code == 200
    assert UserPublic.model_validate(response.json()) == UserPublic.model_validate(user)


@pytest.mark.asyncio
async def test_read_my_user_with_nonexistent_user_id(session: AsyncSession, client: AsyncClient):
    token = create_token(str(uuid.uuid4()))
    response = await client.get(
        URL_USERS + '/me',
        headers={'Authorization': 'Bearer ' + token.access_token},
    )
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_read_my_user_without_token(client: AsyncClient):
    response = await client.get(URL_USERS + '/me')
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated.'}


@pytest.mark.asyncio
async def test_read_my_user_with_invalid_token(client: AsyncClient):
    response = await client.get(URL_USERS + '/me', headers={'Authorization': 'Bearer qwerty'})
    assert response.status_code == 403
    assert response.json() == {'detail': 'Invalid token.'}
