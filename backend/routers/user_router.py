from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from backend.database.db_config import get_db
from backend.schemas import UserOut
from backend.services.userService import get_authed_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
def read_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    user = get_authed_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return user
