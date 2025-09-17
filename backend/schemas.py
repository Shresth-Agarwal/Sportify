from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    age: int
    height: float
    weight: float
    sport: str


class UserOut(BaseModel):
    id: int
    username: str
    age: int
    height: float | None = None
    weight: float | None = None
    sport: str | None = None

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    username: str | None = None
    age: int | None = None
    height: float | None = None
    weight: float | None = None
    sport: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ExerciseCreate(BaseModel):
    name: str


class ExerciseOut(BaseModel):
    id: int
    name: str


class RecordCreate(BaseModel):
    exercise_id: int
    value: float


class RecordOut(BaseModel):
    id: int
    user_id: int
    exercise_id: int
    value: float
    recorded_at: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
