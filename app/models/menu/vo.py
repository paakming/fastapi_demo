from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class MenuVO(BaseModel):
    id: int
    name: str
    code: str
    path: str | None = None
    component: str | None = None
    icon: str | None = None
    parent_id: int | None = None
    sort: int
    is_hidden: int
    created_at: datetime
    updated_at: datetime | None = None
    children: list[MenuVO] = []

    class Config:
        from_attributes = True
