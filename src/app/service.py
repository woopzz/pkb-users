import datetime as dt
import re
import uuid
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request
from passlib.context import CryptContext
from sqlalchemy import select

from app.core.config import settings
from app.core.db import SessionDep

from .constants import JWT_ALGORITHM
from .models import Token, User

auth_header_regex = re.compile('bearer (.*)', flags=re.IGNORECASE)
pwd_context = CryptContext(schemes=['bcrypt'])


async def get_user_by_name(session: SessionDep, name: str):
    stmt = select(User).where(User.name == name)
    return await session.scalar(stmt)


def create_token(sub: str):
    claims = {
        'sub': sub,
        'exp': (dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=settings.JWT_LIFETIME_IN_MINUTES)),
    }
    access_token = jwt.encode(claims, settings.JWT_SECRET, algorithm=JWT_ALGORITHM)
    return Token(access_token=access_token)


def parse_token(token: str):
    try:
        claims = jwt.decode(token, settings.JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return True, claims['sub']
    except jwt.PyJWTError:
        return False, None


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def get_current_user(request: Request, session: SessionDep) -> User:
    token = None

    authorization = request.headers.get('Authorization')
    if authorization:
        match = auth_header_regex.match(authorization)
        if match:
            token = match.groups()[0]

    if not token:
        raise HTTPException(
            status_code=401,
            detail='Not authenticated.',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    ok, user_id = parse_token(token)
    if not ok:
        raise HTTPException(status_code=403, detail='Invalid token.')

    user = await session.get(User, uuid.UUID(user_id))
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]
