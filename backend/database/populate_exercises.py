import json
from sqlalchemy.orm import Session
from backend.models import Exercise
from backend.database.db_config import engine


EXERCISE_JSON_PATH = "backend/data/exercises.json"


def seed_exercises():
    # Read JSON
    with open(EXERCISE_JSON_PATH, "r") as f:
        exercises_data = json.load(f)

    with Session(engine) as session:
        for ex in exercises_data:
            # Check if exercise already exists
            exists = session.query(Exercise).filter_by(name=ex["name"]).first()
            if not exists:
                exercise = Exercise(
                    name=ex["name"],
                    category=ex.get("category"),
                    metric_type=ex.get("metric_type")
                )
                session.add(exercise)

        session.commit()
        print(f"Seeded {len(exercises_data)} exercises (if not already present).")


if __name__ == "__main__":
    seed_exercises()
