from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.database.db_config import get_db
from backend.schemas import UserOut
from backend.services.user_service import get_current_user

bearer = HTTPBearer()

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
def read_current_user(
    credential: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db)
):
    user = get_current_user(credential, db)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    return user
