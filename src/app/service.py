import datetime as dt

import jwt
from sqlalchemy import select

from app.core.config import settings
from app.core.db import SessionDep
from app.core.security import pwd_context

from .constants import JWT_ALGORITHM
from .models import Token, User


async def get_user_by_name(session: SessionDep, name: str):
    stmt = select(User).where(User.name == name)
    return await session.scalar(stmt)


def create_token(sub: str):
    claims = {
        'sub': sub,
        'exp': (
            dt.datetime.now(dt.timezone.utc)
            + dt.timedelta(minutes=settings.JWT_LIFETIME_IN_MINUTES)
        ),
    }
    access_token = jwt.encode(claims, settings.JWT_SECRET, algorithm=JWT_ALGORITHM)
    return Token(access_token=access_token)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)
