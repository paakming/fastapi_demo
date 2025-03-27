from enum import Enum
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field, Relationship
from pydantic import EmailStr, HttpUrl, BaseModel, model_validator, field_serializer

from.role_permisson import RolePermissions
from .user_role import UserRoles

class Role(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field()
    
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    deleted_at: datetime = Field(default=None)

    users: Optional[list["User"]] = Relationship(back_populates="roles", link_model=UserRoles)
    permissions: Optional[list["Permission"]] = Relationship(back_populates="roles", link_model=RolePermissions)