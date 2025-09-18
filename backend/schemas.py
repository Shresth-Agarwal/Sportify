from pydantic import BaseModel, EmailStr
from typing import Any, Dict, Optional
from datetime import datetime
from backend.enums import MetricTypeEnum, CategoryEnum


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    age: int
    height: float | None = None
    weight: float | None = None
    sport: str | None = None


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
    category: Optional[CategoryEnum] = None
    metric_type: Optional[MetricTypeEnum] = None


class ExerciseOut(BaseModel):
    id: int
    name: str
    category: Optional[CategoryEnum] = None
    metric_type: Optional[MetricTypeEnum] = None

    class Config:
        from_attributes = True


class ExerciseRecordBase(BaseModel):
    sets: Optional[int] = None
    reps: Optional[int] = None
    metric_value: Optional[float] = None
    note: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


class ExerciseRecordCreate(ExerciseRecordBase):
    user_id: int
    exercise_id: int


class ExerciseRecordUpdate(ExerciseRecordBase):
    pass


class ExerciseRecordOut(ExerciseRecordBase):
    id: int
    user_id: int
    exercise_id: int
    recorded_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class AnalysisResponse(BaseModel):
    task_id: str
    message: str


class TaskStatus(BaseModel):
    status: str
    result: Optional[str] = None