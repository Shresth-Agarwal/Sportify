import time
import argparse
from backend.ml.video_engine.analysis_engine import ExerciseAnalyzer
from backend.ml.video_engine.exercise_logic import PushupLogic, SquatLogic, PullupLogic
from backend.ml.video_engine.reporting import save_report_as_json

def run_analysis(video_path: str, exercise_type: str, output_path: str):
    """
    Runs the full analysis pipeline and saves the report.
    This is the primary function your frontend team will call.
    """
    print(f"Received request to analyze '{video_path}' for '{exercise_type}'.")
    
    logic_map = {
        'pushup': PushupLogic,
        'squat': SquatLogic,
        'pullup': PullupLogic
    }
    
    if exercise_type not in logic_map:
        raise ValueError(f"Unknown exercise type: {exercise_type}")

    logic = logic_map[exercise_type]()
    
    analyzer = ExerciseAnalyzer(exercise_logic=logic)
    report = analyzer.process_video(video_path)
    
    save_report_as_json(report, output_path)
    
    print("\n" + "="*50)
    print("           ANALYSIS SUMMARY (FOR DEMO)")
    print("="*50)
    print(f"  - Exercise:             {report.exercise_type}")
    print(f"  - Repetition Count:       {report.total_repetitions}")
    print(f"  - Avg. Rep Time:        {report.average_rep_time}s")
    print(f"  - Workout Intensity:      {report.workout_intensity}")
    print(f"  - Form Issues Detected:   {'Yes' if report.form_feedback else 'No'}")
    if report.form_feedback:
        for issue in report.form_feedback:
            print(f"    - {issue}")
    print("="*50)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="AI-Powered Exercise Analysis Engine")
    parser.add_argument("--video", type=str, required=True, help="Path to the video file.")
    parser.add_argument("--exercise", type=str, required=True, choices=['pushup', 'squat', 'pullup'], help="The exercise to analyze.")
    parser.add_argument("--output_json", type=str, default="analysis_report.json", help="Path to save the JSON report.")
    args = parser.parse_args()

    start_time = time.time()
    try:
        run_analysis(args.video, args.exercise, args.output_json)
    except Exception as e:
        print(f"\nAN ERROR OCCURRED: {e}")
        print("Analysis failed. Please check the video file and exercise type.")
    finally:
        end_time = time.time()
        print(f"\nTotal execution time: {end_time - start_time:.2f} seconds.")