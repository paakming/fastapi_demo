from enum import Enum
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field
from pydantic import EmailStr, HttpUrl, BaseModel, model_validator, field_serializer


class RolePermissions(SQLModel, table=True):
    __tablename__ = "role_permissions"

    role_id: int = Field(primary_key=True,foreign_key="role.id")
    permission_id: int = Field(primary_key=True,foreign_key="permission.id")

