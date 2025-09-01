from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class RoleVO(BaseModel):
    id: int
    name: str
    code: str
    is_admin: bool = False
    is_super_admin: bool = False
    created_at: datetime
    updated_at: datetime
    # menus: list[dict] = []

    class Config:
        from_attributes = True
