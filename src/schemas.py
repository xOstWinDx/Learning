import datetime

from pydantic import ConfigDict, BaseModel, EmailStr, Field


class BaseSchema(BaseModel):
    id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class UserBase(BaseModel):
    email: EmailStr | None
    name: str = Field(max_length=32, min_length=3)
