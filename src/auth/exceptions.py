from fastapi import HTTPException
from starlette import status


class IncorrectPasswordAuthExc(ValueError):
    def __init__(self):
        super().__init__("Incorrect Password")


class NotEnoughRightsAuthExc(ValueError):
    def __init__(self):
        super().__init__("Not enough rights")


class InvalidCredentialsAuthExc(HTTPException):
    def __init__(self):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid pass or login")


