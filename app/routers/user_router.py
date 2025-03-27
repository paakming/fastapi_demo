from fastapi import APIRouter
from enum import Enum
from typing import Annotated, Literal, Any
from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from pydantic import BaseModel, Field, EmailStr, HttpUrl

from sqlmodel import col, delete, func, select

from app.models.user import UserIn, UserVO, User
from app.models.response_result import ResponResult
from .deps import SessionDep

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/", response_model=ResponResult)
async def get_users(session: SessionDep, page_num: int  = Query(1, ge=1), page_size: int = Query(10, ge=10), order: str = Query("asc")) -> ResponResult:
    statment = select(User).offset((page_num - 1) * page_size).limit(page_size)
    users = session.exec(statment).all()
    user_vos = [UserVO.model_validate(user) for user in users]
    user_dicts = [user_vo.model_dump() for user_vo in user_vos]
    return ResponResult.success(msg="success", result=user_dicts)


@router.get("/{user_id}", response_model=ResponResult)
async def get_user(session: SessionDep,user_id: int):
    """
    permissions: {
        "perms": [],
        "paths": [],
        "components": []
    }
    """
    statment = select(User).where(User.id == user_id)
    user = session.exec(statment).first()
    if not user:
        return ResponResult.error(msg="user not found")
    roles = [role.name for role in user.roles]
    permissions = [role.permissions for role in user.roles]
    return {"item_id": user_id}


@router.post("/", response_model=ResponResult)
async def create_user(session: SessionDep, user: UserIn) -> ResponResult:
    return user


