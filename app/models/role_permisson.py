from sqlmodel import Field, SQLModel


class RolePermissions(SQLModel, table=True):
    __tablename__ = "role_permissions"

    role_id: int = Field(primary_key=True, foreign_key="role.id")
    permission_id: int = Field(primary_key=True, foreign_key="permission.id")
