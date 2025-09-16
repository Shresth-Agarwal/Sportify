from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.database.db_config import get_db
from backend.schemas import UserOut
from backend.services.userService import get_authed_user

bearer = HTTPBearer()

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
def read_current_user(
    credential: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db)
):
    token = credential.credentials
    user = get_authed_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return user
