import uuid

from src.users.repository import UserRepository
from src.users.schemas import UserAll
from src.users.service import UserService


class AuthService(UserService):

    def __init__(self, repository: UserRepository):
        super().__init__(repository)

    async def get_one_or_none(
            self,
            id: uuid.UUID | None = None,  # noqa
            email: str | None = None,
            name: str | None = None,
            is_admin: bool | None = None
    ) -> UserAll | None:
        return UserAll.model_validate(
            await self.repository.get_one_or_none(
                id=id,
                email=email,
                name=name,
                is_admin=is_admin
            )
        )
