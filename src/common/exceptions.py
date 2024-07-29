from fastapi import HTTPException
from starlette import status


class ForbiddenAuthExc(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough rights")


class UnknownUserAuthExc(ValueError):
    def __init__(self):
        super().__init__("User unknown")


class InvalidTokenAuthExc(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
