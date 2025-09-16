from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.models import User, Auth
from backend.schemas import UserCreate
from backend.auth_utils import get_password_hash
from backend.database.db_config import get_db
from backend.services.jwt_service import verify_jwt_token


bearer = HTTPBearer()


def get_user_by_email(db: Session, email: str) -> User | None:
    return (
        db.query(User)
        .join(Auth, User.id == Auth.user_id)
        .filter(Auth.email == email)
        .first()
    )


def create_user(db: Session, user_in: UserCreate) -> User:
    # Check duplicate email in auth table
    existing_auth = db.query(Auth).filter(Auth.email == user_in.email).first()
    if existing_auth:
        raise HTTPException(status_code=400, detail="Email already registered")

# Auth Table
    hashed_pw = get_password_hash(user_in.password)

    # User table
    new_user = User(
        username=user_in.username,
        height=user_in.height,
        weight=user_in.weight,
        age=user_in.age,
        sport=user_in.sport
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Auth Table
    db_auth = Auth(
        user_id=new_user.id,
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed_pw,
    )
    db.add(db_auth)
    db.commit()

    return new_user


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db)
) -> User:
    user_id = verify_jwt_token(credentials)
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    return user
