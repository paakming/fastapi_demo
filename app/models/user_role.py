from enum import Enum
from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel, Field
from pydantic import EmailStr, HttpUrl, BaseModel, model_validator, field_serializer


class UserRoles(SQLModel, table=True):
    __tablename__ = "user_roles"

    user_id: int = Field(primary_key=True,foreign_key="user.id")
    role_id: int = Field(primary_key=True,foreign_key="role.id")

