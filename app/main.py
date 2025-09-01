from fastapi import FastAPI

from app.routers import role_router, user_router

app = FastAPI()
app.include_router(user_router.router)
app.include_router(role_router.router)


@app.get("/")
async def main():
    return "Hello World"


# uvicorn app.main:app --host 0.0.0.0 --port 8080 --reload
# fastapi dev app/main --host 0.0.0.0 --port 8080 --reload
