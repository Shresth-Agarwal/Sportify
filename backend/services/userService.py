from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.models import User, Auth
from backend.schemas import UserCreate
from backend.auth_utils import get_password_hash, verify_password
from backend.token import verify_access_token


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


def verify_user_credentials(db: Session, email: str, password: str) -> User:
    auth = db.query(Auth).filter(Auth.email == email).first()
    if not auth or not verify_password(password, auth.hashed_password):  # type: ignore
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return auth.user


def get_authed_user(db: Session, token: str) -> User:
    payload = verify_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token missing subject (user_id)",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user
