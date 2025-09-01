from pydantic import BaseModel


class MenuCreateDTO(BaseModel):
    name: str | None = None
    code: str | None = None
    path: str | None = None
    component: str | None = None
    perms: str | None = None
    icon: str | None = None
    parent_id: int | None = None
    sequence: int | None = None
    is_visible: int | None = None


class MenuUpdateDTO(BaseModel):
    id: int
    name: str | None = None
    code: str | None = None
    path: str | None = None
    component: str | None = None
    perms: str | None = None
    icon: str | None = None
    parent_id: int | None = None
    sequence: int | None = None
    is_visible: int | None = None
