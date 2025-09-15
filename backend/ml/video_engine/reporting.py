import json
from dataclasses import dataclass, asdict
from typing import List

@dataclass
class RepDetail:
    """Stores detailed metrics for a single repetition."""
    rep_number: int
    time_taken: float
    min_angle: float

@dataclass
class AnalysisReport:
    """A structured dataclass for the final analysis report."""
    exercise_type: str
    total_repetitions: int
    workout_duration_sec: float
    average_pace_reps_per_sec: float
    form_feedback: List[str]
    rep_details: List[RepDetail]

def save_report_as_json(report: AnalysisReport, output_path: str):
    """Saves the AnalysisReport to a JSON file."""
    print(f"\nSaving detailed report to: {output_path}")
    with open(output_path, 'w') as f:
        json.dump(asdict(report), f, indent=4)