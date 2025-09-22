from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.service import get_password_hash


async def create_user(session: AsyncSession, **values) -> User:
    values.setdefault('name', 'test')
    values.setdefault('password', 'testtest')

    values['password'] = get_password_hash(values['password'])
    user = User(**values)

    session.add(user)
    await session.commit()
    return user
