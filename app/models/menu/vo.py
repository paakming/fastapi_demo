from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class MenuVO(BaseModel):
    id: int
    name: str
    code: str
    path: str | None = None
    component: str | None = None
    perms: str | None = None
    icon: str | None = None
    parent_id: int | None = None
    sequence: int
    is_visible: int
    type: int
    created_at: datetime
    updated_at: datetime | None = None
    children: list[MenuVO] = []

    class Config:
        from_attributes = True
