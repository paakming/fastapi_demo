from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core import database
from app.core.config import settings
from app.core.redis import close_redis
from app.exception import global_excetption_handler
from app.router import (
    auth_router,
    # menu_router,
    role_router,
    user_router,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动事件
    if settings.APP_ENV == 'dev' and settings.AUTO_CREATE_TABLE:
        await database.init_create_table()
    yield
    # 关闭事件
    await close_redis()


app = FastAPI(lifespan=lifespan)
global_excetption_handler(app)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

host = settings.APP_HOST
port = settings.APP_PORT
reload = settings.APP_RELOAD

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(role_router)
# app.include_router(menu_router)


@app.get('/')
async def main():
    return 'FastAPI Demo'
