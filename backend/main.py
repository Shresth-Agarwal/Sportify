from video_engine.analysis_engine import ExerciseAnalyzer

if __name__ == '__main__':
    # --- CONFIGURATION ---
    video_path = 'video.mp4'  # The video you want to analyze
    exercise_type = 'pushup'    # The exercise type ('pushup', 'squat', etc.)

    # --- EXECUTION ---
    # 1. Initialize the analyzer with the type of exercise
    analyzer = ExerciseAnalyzer(exercise_type=exercise_type)
    
    # 2. Run the fast, robust analysis and get the report
    analyzer.process_video(video_path=video_path)