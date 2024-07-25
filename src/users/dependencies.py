from src.database import session_factory
from src.users.service import UserService


def get_user_service() -> UserService:
    return UserService(session_factory=session_factory)
