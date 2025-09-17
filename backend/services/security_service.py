from fastapi import HTTPException
from sqlalchemy.orm import Session
from backend.models import Auth
from backend.utils.auth_utils import verify_password


def verify_user_credentials(db: Session, email: str, password: str) -> int:
    auth = db.query(Auth).filter(Auth.email == email).first()
    if not auth or not verify_password(password, auth.hashed_password):  # type: ignore
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return auth.user.id
