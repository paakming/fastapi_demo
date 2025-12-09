from pydantic import BaseModel

from .user import PrueUserVO


class SecurityUser(BaseModel):
    user: PrueUserVO
    roles: list[str] | None = None
    permissions: list[str] | None = None

    class Config:
        from_attributes = True
