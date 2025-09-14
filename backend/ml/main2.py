from video_engine.analysis_2 import ExerciseAnalyzer
import time

if __name__ == '__main__':
    # --- CONFIGURATION ---
    video_path = 'video.mp4'
    exercise_type = 'pushup'

    # --- EXECUTION ---
    start_time = time.time()
    
    analyzer = ExerciseAnalyzer(exercise_type=exercise_type)
    
    # Pass 1: Extract angle data from the video
    angle_data, fps, total_frames = analyzer.process_video_and_extract_angles(video_path)
    
    if angle_data:
        # Pass 2: Analyze the extracted data to find reps and metrics
        analysis_results = analyzer.analyze_reps_from_angle_data(angle_data, fps)
        
        # Pass 3: Generate the final report
        workout_duration = total_frames / fps
        analyzer.generate_report(analysis_results, workout_duration)

    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds.")