from fastapi import APIRouter, HTTPException

from app.core.db import SessionDep
from app.core.response import generate_openapi_error_responses
from app.service import CurrentUserDep, get_password_hash

from .models import Credentials, Token, User, UserCreate, UserPublic
from .service import create_token, get_user_by_name, verify_password

router = APIRouter()


@router.post(
    '/users',
    response_model=UserPublic,
    responses=generate_openapi_error_responses({400}),
    tags=['user'],
)
async def create_user(*, session: SessionDep, user_in: UserCreate):
    if await get_user_by_name(session, user_in.name):
        raise HTTPException(status_code=400, detail='This username is already taken.')

    password = get_password_hash(user_in.password.get_secret_value())
    user = User(name=user_in.name, password=password)
    session.add(user)
    await session.commit()
    return UserPublic.model_validate(user)


@router.get(
    '/users/me',
    response_model=UserPublic,
    responses=generate_openapi_error_responses(set(), add_token_related_errors=True),
    tags=['user'],
)
async def read_my_user(*, current_user: CurrentUserDep):
    return UserPublic.model_validate(current_user)


@router.post(
    '/access-token',
    response_model=Token,
    responses=generate_openapi_error_responses({404}),
    tags=['auth'],
)
async def create_access_token(*, session: SessionDep, creds: Credentials):
    user = await get_user_by_name(session, creds.name)
    if not (user and verify_password(creds.password.get_secret_value(), user.password)):
        raise HTTPException(status_code=404, detail='User not found.')

    return create_token(str(user.id))
