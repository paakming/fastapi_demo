from sqlmodel import Field, SQLModel


class UserRoles(SQLModel, table=True):
    __tablename__ = "user_roles"

    user_id: int = Field(primary_key=True, foreign_key="user.id")
    role_id: int = Field(primary_key=True, foreign_key="role.id")
