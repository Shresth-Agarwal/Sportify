import os
import json
from backend.ml.main import run_analysis
from backend.services.ml_summary import get_ai_summary

# In-memory dictionary to act as a simple database for task statuses.
# For a production app, you would use Redis, Celery, or a database.
task_statuses = {}

def run_full_analysis(video_path: str, exercise_type: str, task_id: str):
    """
    The main background task function. It runs the entire pipeline.
    """
    json_output_path = f"{os.path.splitext(video_path)[0]}_report.json"
    
    try:
        # Step 1: Set initial status
        task_statuses[task_id] = {"status": "processing", "result": None}

        # Step 2: Run the computer vision analysis from your existing engine
        # Note: This is a synchronous call, it will block until it's done.
        run_analysis(video_path, exercise_type, json_output_path)

        # Step 3: Read the resulting JSON report
        with open(json_output_path, 'r') as f:
            analysis_data = json.load(f)
        
        # Step 4: Convert the dictionary to a JSON string for the AI prompt
        analysis_json_string = json.dumps(analysis_data)
        
        # Step 5: Get the user-friendly summary from the AI model
        ai_summary = get_ai_summary(analysis_json_string)
        
        # Step 6: Update the task status to 'complete' with the final result
        task_statuses[task_id] = {"status": "complete", "result": ai_summary}

    except Exception as e:
        print(f"An error occurred during analysis for task {task_id}: {e}")
        task_statuses[task_id] = {"status": "failed", "result": str(e)}
        
    finally:
        # Step 7: Clean up the temporary files
        if os.path.exists(video_path):
            os.remove(video_path)
        if os.path.exists(json_output_path):
            os.remove(json_output_path)