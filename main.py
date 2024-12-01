from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes import student_routes
from app.database import Database
import uvicorn


@asynccontextmanager
async def lifespan(app: FastAPI):
    await Database.connect_database()
    yield
    await Database.close_database()

app = FastAPI(
    title="Student Management System",
    lifespan=lifespan
)

@app.get("/")
async def read_root():
    return "Welcome to Student-management Backend"

app.include_router(student_routes.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)