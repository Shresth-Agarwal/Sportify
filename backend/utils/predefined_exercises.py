import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXERCISE_JSON_PATH = os.path.join(BASE_DIR, "data", "exercises.json")

# Load JSON once at import
with open(EXERCISE_JSON_PATH, "r") as f:
    PREDEFINED_EXERCISES = {ex["name"].lower(): ex for ex in json.load(f)}


def get_predefined_exercises(name: str):
    """Return exercise data from JSON or None if not found"""
    return PREDEFINED_EXERCISES.get(name.lower())
