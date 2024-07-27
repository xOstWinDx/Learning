from typing import Any

from pydantic import BaseModel, UUID4, EmailStr, Field


class JwtPayload(BaseModel):
    id: UUID4
    name: str

    def model_dump(self, *args, **kwargs) -> dict[str, Any]:
        d = super().model_dump(*args, **kwargs)
        d["id"] = str(d["id"])
        return d


class UserAuth(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
