from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from .role_permisson import RolePermissions
from .user_role import UserRoles


class Role(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True, index=True)
    name: str = Field()

    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(default=datetime.now())
    deleted_at: datetime = Field(default=None)

    users: list["User"] | None = Relationship(
        back_populates="roles", link_model=UserRoles,
    )
    permissions: list["Permission"] | None = Relationship(
        back_populates="roles", link_model=RolePermissions,
    )
