from fastapi import APIRouter
from enum import Enum
from typing import Annotated, Literal, Any
from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from pydantic import BaseModel, Field, EmailStr, HttpUrl

router = APIRouter(
    prefix="/role",
    tags=["role"]
)

@router.get("/")
async def read_role():
    return {"role": "admin"}