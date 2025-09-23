import uuid

from pydantic import Field, SecretStr
from sqlalchemy import types
from sqlalchemy.orm import Mapped, mapped_column

from app.core.models import AuditMixin, BaseSchema, BaseSQLModel, PrimaryUUIDMixin

from .constants import (
    BCRYPT_HASH_LENGTH,
    USER_NAME_MAX_LENGTH,
    USER_NAME_MIN_LENGTH,
    USER_PASSWORD_MIN_LENGTH,
)


class User(PrimaryUUIDMixin, AuditMixin, BaseSQLModel):
    name: Mapped[str] = mapped_column(
        types.String(USER_NAME_MAX_LENGTH),
        nullable=False,
        unique=True,
    )
    password: Mapped[str] = mapped_column(types.String(BCRYPT_HASH_LENGTH), nullable=False)


class UserCreate(BaseSchema):
    name: str = Field(min_length=USER_NAME_MIN_LENGTH, max_length=USER_NAME_MAX_LENGTH)
    password: SecretStr = Field(min_length=USER_PASSWORD_MIN_LENGTH)


class UserPublic(BaseSchema):
    id: uuid.UUID
    name: str


class Token(BaseSchema):
    access_token: str
    token_type: str = 'bearer'


class Credentials(BaseSchema):
    name: str
    password: SecretStr
