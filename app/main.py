from enum import Enum
from typing import Annotated, Literal, Any
from fastapi import FastAPI, Query, Path, Body, Cookie, Header
from pydantic import BaseModel, Field, EmailStr, HttpUrl

from app.routers import role_router, user_router

app = FastAPI()
app.include_router(user_router.router)
app.include_router(role_router.router)

@app.get("/")
def read_root():
    return "Hello World"

# uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
# fastapi dev app/main --host 0.0.0.0 --port 8080 --reload

