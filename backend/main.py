import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from backend.routers import auth, user_router, exercise_router
from backend.routers.ml_router import router as analysis_router
import os


@asynccontextmanager
async def lifespan(app: FastAPI):
    UPLOADS_DIR = "uploads"
    if not os.path.exists(UPLOADS_DIR):
        os.makedirs(UPLOADS_DIR)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(auth.router)
app.include_router(user_router.router)
app.include_router(exercise_router.router)
app.include_router(analysis_router)

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)


@app.get("/")
async def read_root():
    return {"message": "Welcome to the AI Fitness Coach API!"}
