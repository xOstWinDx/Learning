from .router import router as users_router
from src.auth import auth_router

users_router.include_router(auth_router)

__all__ = ["users_router"]
