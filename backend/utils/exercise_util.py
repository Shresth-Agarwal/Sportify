from sqlalchemy.orm import Session
from sqlalchemy import func
from backend.models import Exercise, ExerciseRecord


def get_pr(db: Session, user_id: int, exercise_name: str):
    # Fetch the exercise metadata
    exercise = db.query(Exercise).filter(Exercise.name == exercise_name).first()
    if not exercise:
        return None

    # For time-based exercises
    if exercise.metric_type == "time":  # type: ignore
        pr = db.query(func.min(ExerciseRecord.metric_value)).filter(
            ExerciseRecord.user_id == user_id,
            ExerciseRecord.exercise_id == exercise.id
        ).scalar()
    else:  # For other exercise types
        pr = db.query(func.max(ExerciseRecord.metric_value)).filter(
            ExerciseRecord.user_id == user_id,
            ExerciseRecord.exercise_id == exercise.id
        ).scalar()

    return {
        "exercise": exercise.name,
        "metric_type": exercise.metric_type,
        "pr": pr
    }
