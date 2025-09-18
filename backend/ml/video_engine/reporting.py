import json
from dataclasses import dataclass, asdict
from typing import List, Tuple

@dataclass
class AnalysisReport:
    """
    A structured dataclass for the final analysis report.
    This version is optimized for generating a high-level summary.
    """
    exercise_type: str
    total_repetitions: int
    workout_duration_sec: float
    average_rep_time: float
    min_angle_range: Tuple[float, float]
    workout_intensity: str  # e.g., 'Low', 'Moderate', 'High'
    form_feedback: List[str]

def save_report_as_json(report: AnalysisReport, output_path: str):
    """Saves the AnalysisReport to a JSON file."""
    print(f"\nSaving detailed report to: {output_path}")
    with open(output_path, 'w') as f:
        json.dump(asdict(report), f, indent=4)