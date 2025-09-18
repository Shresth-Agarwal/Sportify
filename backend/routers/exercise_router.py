from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from backend.schemas import ExerciseCreate, ExerciseOut
from backend.services import exercise_service
from backend.database.db_config import get_db


router = APIRouter(prefix="/exercises", tags=["Exercises"])


@router.post("/", response_model=ExerciseOut)
def create_exercise(exercise_in: ExerciseCreate, db: Session = Depends(get_db)):
    return exercise_service.create_exercise(exercise_in, db)


@router.get("/{name}", response_model=ExerciseOut)
def get_exercise_by_name(name: str, db: Session = Depends(get_db)):
    return exercise_service.get_exercise_by_name(name, db)


@router.get("/", response_model=list[ExerciseOut])
def get_all_exercises(db: Session = Depends(get_db)):
    return exercise_service.get_all_exercises(db)


@router.delete("/{exercise_id}", response_model=dict)
def delete_exercise(exercise_id: int, db: Session = Depends(get_db)):
    exercise_service.delete_exercise(exercise_id, db)
    return {"detail": "Exercise deleted successfully"}
