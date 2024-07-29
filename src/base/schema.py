import datetime

from pydantic import  ConfigDict, BaseModel


class BaseSchema(BaseModel):
    id: int
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
