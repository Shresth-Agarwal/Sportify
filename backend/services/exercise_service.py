from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from backend.models import Exercise
from backend.schemas import ExerciseCreate
from backend.database.db_config import get_db


def create_exercise(exercise_in: ExerciseCreate, db: Session = Depends(get_db)) -> Exercise:
    existing_exercise = db.query(Exercise).filter(Exercise.name == exercise_in.name).first()
    if existing_exercise:
        raise HTTPException(status_code=400, detail="Exercise already exists")

    new_exercise = Exercise(name=exercise_in.name.lower())
    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)
    return new_exercise


def get_exercise_by_name(name: str, db: Session = Depends(get_db)) -> Exercise | None:
    exercise = db.query(Exercise).filter(Exercise.name == name).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return exercise


def get_all_exercises(db: Session = Depends(get_db)) -> list[Exercise]:
    e_list = db.query(Exercise).all()
    if e_list is None:
        raise HTTPException(status_code=404, detail="No exercises found")
    return e_list


def delete_exercise(exercise_id: int, db: Session = Depends(get_db)) -> None:
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found")
    db.delete(exercise)
    db.commit()
