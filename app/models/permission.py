from datetime import datetime

from pydantic import BaseModel
from sqlmodel import Field, Relationship, SQLModel

from .role import Role
from .role_permisson import RolePermissions


class Permission(SQLModel, table=True):

    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field()
    path: str = Field()
    perm: str = Field()
    component: str | None = Field()
    parent_id: int | None = Field()

    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    deleted_at: datetime = Field(default=None)

    roles: list["Role"] | None = Relationship(
        back_populates="permissions",
        link_model=RolePermissions,
    )


class UserPerms(BaseModel):
    perms: list[str]
    components: list[str]
    paths: list[str]