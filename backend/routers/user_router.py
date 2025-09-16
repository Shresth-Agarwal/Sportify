from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.database.db_config import get_db
from backend.schemas import UserOut, UserUpdate
from backend.services import user_service

bearer = HTTPBearer()

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
def read_current_user(
    credential: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db)
):
    user = user_service.get_current_user(credential, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return user


@router.get("/{id}", response_model=UserOut)
def get_user_by_id(id: int, db: Session = Depends(get_db)):
    return user_service.get_user_by_id(db, id)


@router.put("/update", response_model=UserOut)
def update_current_user(
    user_in: UserUpdate,
    credential: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db)
):
    user = user_service.update_current_user(user_in, credential, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return user


@router.put("/update/{id}", response_model=UserOut)
def update_user_by_id(id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    return user_service.update_user_by_id(db, id, user_in)


@router.delete("/delete", response_model=dict)
def delete_current_user(
    credential: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db)
):
    return user_service.delete_current_user(credential, db)


@router.delete("/{id}", response_model=dict)
def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    return user_service.delete_user_by_id(db, id)
