import uvicorn
from fastapi import FastAPI
from backend.routers import auth, user_router, exercise_router

app = FastAPI()

app.include_router(auth.router)
app.include_router(user_router.router)
app.include_router(exercise_router.router)


if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
