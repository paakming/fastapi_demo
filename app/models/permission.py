from enum import Enum
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, HttpUrl, BaseModel, model_validator, field_serializer

from.role_permisson import RolePermissions


class Permission(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field()
    path: str = Field()
    perm: str = Field()
    component: Optional[str] = Field()
    parent_id: Optional[int] = Field()
    
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    deleted_at: datetime = Field(default=None)

    roles: Optional[list["Role"]] = Relationship(back_populates="permissions", link_model=RolePermissions)


class UserPerms(BaseModel):
    perms: list[str]
    components: list[str]
    paths: list[str]
    