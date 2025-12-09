from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, field_validator

from app.models.menu import MenuVO


class RoleVO(BaseModel):
    id: int
    name: str
    code: str
    is_admin: bool = False
    is_super_admin: bool = False
    created_at: datetime
    updated_at: datetime
    menus: list[MenuVO] = []

    @field_validator('menus', mode='before')
    @classmethod
    def validate_menus(cls, v):
        if v is None:
            return []
        return [MenuVO.model_validate(menu) for menu in v]

    class Config:
        from_attributes = True


class UserRoleVO(BaseModel):
    id: int
    name: str
    code: str
    is_admin: bool = False
    is_super_admin: bool = False

    class Config:
        from_attributes = True
