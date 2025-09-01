from datetime import datetime

from pydantic import BaseModel, field_validator

from app.exception.service_exception import ServiceException

from ..base import BaseCreateDTO, BaseUpdateDTO


class UserCreateDTO(BaseCreateDTO):
    username: str
    email: str
    password: str
    gender: str | None
    birthday: str | None
    nickname: str | None
    phone: str | None

    @field_validator('birthday')
    @classmethod
    def format_birthday(cls, v):
        if v is None or v == '':
            return None
        if isinstance(v, str):
            try:
                return datetime.strptime(v, '%Y-%m-%d')
            except ValueError:
                raise ServiceException(message='Invalid birthday format')


class UserUpdateDTO(BaseUpdateDTO):
    id: int
    email: str | None
    gender: str | None
    birthday: str | None
    nickname: str | None
    phone: str | None
    avatar: str | None = None


class UserLoginDTO(BaseModel):
    username: str
    password: str


class PassWordChangeDTO(BaseModel):
    id: int
    old_password: str
    new_password: str
