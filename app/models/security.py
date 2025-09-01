from pydantic import BaseModel

from .user import UserVO


class SecurityUser(BaseModel):
    user: UserVO
    roles: list[str] | None = None
    permissions: list[str] | None = None

    class Config:
        from_attributes = True
