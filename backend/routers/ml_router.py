import uuid
import os
from fastapi import APIRouter, UploadFile, File, Form, BackgroundTasks, HTTPException
from backend.schemas import AnalysisResponse, TaskStatus
from backend.services.ml_video import run_full_analysis, task_statuses

router = APIRouter(prefix="/ml", tags=["Analysis"])
UPLOADS_DIR = "uploads"


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_video(
    background_tasks: BackgroundTasks,
    exercise_type: str = Form(...),
    video: UploadFile = File(...)
):
    """
    This endpoint accepts a video and an exercise type,
    saves the video, and starts the analysis in the background.
    """
    # Generate a unique ID for this analysis task
    task_id = str(uuid.uuid4())

    # Define the path to save the uploaded video
    video_path = os.path.join(UPLOADS_DIR, f"{task_id}_{video.filename}")

    # Save the video file
    with open(video_path, "wb") as buffer:
        buffer.write(await video.read())

    # Add the long-running analysis function to the background tasks
    background_tasks.add_task(run_full_analysis, video_path, exercise_type, task_id)

    # Immediately return the task ID to the client
    return {"task_id": task_id, "message": "Analysis has started."}


@router.get("/status/{task_id}", response_model=TaskStatus)
async def get_analysis_status(task_id: str):
    """
    This endpoint allows the client to poll for the status
    of an analysis task using its ID.
    """
    status = task_statuses.get(task_id)
    if not status:
        raise HTTPException(status_code=404, detail="Task not found")

    return status
