import uuid

from pydantic import EmailStr, Field, field_validator, BaseModel, PrivateAttr
from pydantic.json_schema import SkipJsonSchema

from src.base import BaseSchema
from src.users.utils import hash_password


class UserPublic(BaseModel):
    email: EmailStr
    name: str = Field(max_length=32, min_length=3)


class UserPrivate(UserPublic):
    hashed_password: str | SkipJsonSchema[bytes] = Field(alias="password", min_length=8)

    @field_validator("hashed_password")
    def hash_pass(cls, v):
        return hash_password(v)


class UserCreate(UserPrivate):
    # Приватное поле для хранения
    _id: uuid.UUID = PrivateAttr(default_factory=uuid.uuid4)
    _is_admin: bool = PrivateAttr(default=False)

    def model_dump(self, *args, **kwargs):
        d = super().model_dump(*args, **kwargs)
        d['id'] = str(self._id)
        d['is_admin'] = self._is_admin
        return d


class UserRead(BaseSchema, UserPublic):
    is_admin: bool
