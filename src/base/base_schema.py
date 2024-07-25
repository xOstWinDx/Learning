import datetime
import uuid

from pydantic import UUID4, ConfigDict, BaseModel


class BaseSchema(BaseModel):
    id_: UUID4 = uuid.uuid4()
    created_at: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
