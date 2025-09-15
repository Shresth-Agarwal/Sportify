from video_engine.analysis_engine import ExerciseAnalyzer, PushupLogic, SquatLogic
import time

if __name__ == '__main__':
    # --- CHOOSE YOUR EXERCISE AND VIDEO HERE ---
    
    # Option 1: Analyze Push-ups
    video_path = 'video.mp4'  # Use your push-up video
    exercise_type = 'pushup'
    
    # Option 2: Analyze Squats 
    # video_path = 'your_squat_video.mp4' # You'll need a squat video
    # exercise_type = 'squat'

    start_time = time.time()
    
    # Select the correct logic plugin based on the choice
    if exercise_type == 'pushup':
        logic = PushupLogic()
    elif exercise_type == 'squat':
        logic = SquatLogic()
    else:
        raise ValueError("Unknown exercise type specified")

    # The engine is initialized with the chosen logic
    analyzer = ExerciseAnalyzer(exercise_logic=logic)
    
    # Pass 1: Extract data from the video
    angle_data, form_feedback, fps, total_frames = analyzer.process_video_and_extract_data(video_path)
    
    if angle_data:
        # Pass 2: Analyze the extracted data for reps
        analysis_results = analyzer.analyze_reps_from_angle_data(angle_data, fps)
        
        # Pass 3: Generate the final, combined report
        workout_duration = total_frames / fps
        analyzer.generate_report(analysis_results, form_feedback, workout_duration)

    end_time = time.time()
    print(f"\nTotal execution time: {end_time - start_time:.2f} seconds.")