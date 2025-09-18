from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.models import User, Auth
from backend.schemas import UserCreate, UserUpdate
from backend.utils.auth_utils import get_password_hash
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


def get_user_by_id(db: Session, user_id: int) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def update_current_user(
        user_in: UserUpdate,
        credentials: HTTPAuthorizationCredentials = Depends(bearer),
        db: Session = Depends(get_db),
) -> User:
    user = get_current_user(credentials, db)

    update_user = user_in.model_dump(exclude_unset=True)

    for key, value in update_user.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def update_user_by_id(db: Session, user_id: int, user_in: UserUpdate) -> User:
    user = get_user_by_id(db, user_id)

    update_data = user_in.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(bearer),
        db: Session = Depends(get_db)
) -> dict:
    user = get_current_user(credentials, db)

    db.query(Auth).filter(Auth.user_id == user.id).delete()
    db.query(User).filter(User.id == user.id).delete()
    db.commit()

    return {"detail": "User deleted successfully"}


def delete_user_by_id(db: Session, user_id: int) -> dict:
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.query(Auth).filter(Auth.user_id == user.id).delete()
    db.query(User).filter(User.id == user.id).delete()
    db.commit()

    return {"detail": "User deleted successfully"}
