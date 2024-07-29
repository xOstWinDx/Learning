import bcrypt
import jwt

from src.config import CONFIG
from src.common.schemas import JwtPayload

def encode_jwt(payload: JwtPayload) -> str:
    return jwt.encode(
        payload=payload.model_dump(),
        key=CONFIG.JWT_SECRET_KEY,
        algorithm=CONFIG.JWT_ALGORITHM
    )


