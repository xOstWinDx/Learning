import datetime

from pydantic import UUID4, ConfigDict, BaseModel


class BaseSchema(BaseModel):
    id: UUID4
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
