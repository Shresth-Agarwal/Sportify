from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database.db_config import get_db
from backend import schemas
from backend.token import create_access_token
from backend.services import user_service, security_service

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    return user_service.create_user(db, user_in)


@router.post("/login", response_model=schemas.Token)
def login(user_in: schemas.UserLogin, db: Session = Depends(get_db)):
    user_id = security_service.verify_user_credentials(db, user_in.email, user_in.password)

    access_token = create_access_token(data={"sub": str(user_id)})  # type: ignore
    return {"access_token": access_token, "token_type": "bearer"}
