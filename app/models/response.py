from enum import IntEnum
from typing import Any

from pydantic import BaseModel


class ResponseCode(IntEnum):
    SUCCESS = 200
    ERROR = 500
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    BAD_REQUEST = 400


class ResultResponse(BaseModel):
    code: int
    message: str
    data: Any | None

    class Config:
        from_attributes = True

    @classmethod
    def success(
        cls,
        code: int = ResponseCode.SUCCESS,
        message: str = 'success',
        data: BaseModel | Any | None = None,
        is_model: bool = True,
    ):
        if is_model and isinstance(data, BaseModel):
            data = data.model_dump() if data else None
        return cls(code=code, message=message, data=data)

    @classmethod
    def error(
        cls,
        code: int = ResponseCode.ERROR,
        message: str = 'error',
        data=None,
    ):
        return cls(code=code, message=message, data=data)


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str | None = 'bearer'
    expires_in: int | None = None

    @classmethod
    def success(
        cls,
        access_token: str,
        refresh_token: str,
        token_type: str | None = 'bearer',
        expires_in: int | None = None,
    ):
        return cls(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
            expires_in=expires_in,
        )

    @classmethod
    def error(cls, code: int = ResponseCode.ERROR, message: str = 'error'):
        return cls(access_token='', refresh_token='')
