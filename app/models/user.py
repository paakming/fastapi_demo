from enum import Enum
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, HttpUrl, BaseModel, model_validator, field_serializer

from .user_role import UserRoles
from .permission import UserPerms

class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"
    OTHER = "unknown"

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    username: str = Field()
    nickname: str = Field()
    password: str = Field()
    email: str = Field()
    avatar: str = Field()
    identity: str = Field()
    gender: str = Field(default=GenderEnum.OTHER)
    phone: Optional[str] = Field()
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    deleted_at: datetime = Field(default=None)

    roles: Optional[list['Role']] = Relationship(back_populates="users", link_model=UserRoles)


class UserIn(BaseModel):
    username: str
    password: str
    email: str
    full_name: str | None = None


class UserVO(BaseModel):
    id: int = Field()
    username: str = Field()
    nickname: str = Field()
    email: str = Field()
    avatar: str = Field()
    identity: str = Field()
    gender: str = Field()
    phone: Optional[str] = Field()

    # roles: Optional[list[str]] = Field()
    # permissions: Optional[list[UserPerms]] = Field()

    class Config:
        from_attributes = True

    
    @field_serializer('username', 'nickname', 'email', 'avatar', 'identity', 'gender', 'phone')
    def serialize_none_as_empty_str(self, v):
        return v if v is not None else ""

    # @field_serializer('roles', 'permissions')
    # def serialize_none_as_empty_list(self, v):
    #     return v if v is not None else []
