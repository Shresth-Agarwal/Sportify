from enum import Enum


class CategoryEnum(str, Enum):
    strength = "Strength"
    core = "Core"
    athletics = "Athletics"
    cardio = "Cardio"
    custom = "Custom"


class MetricTypeEnum(str, Enum):
    weight = "weight"
    reps = "reps"
    duration = "duration"
    time = "time"
    distance = "distance"
    height = "height"
    custom = "reps"
