from fastapi import FastAPI

from app.router.auth import router as auth_router

app = FastAPI(
    title="User Authentication API",
    description="A simple user authentication API built with FastAPI and SQLAlchemy.",
)

app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the User Authentication API!"}
