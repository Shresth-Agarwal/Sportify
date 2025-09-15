import cv2
import numpy as np
import mediapipe as mp
from scipy.signal import find_peaks
from video_engine.exercise_logic import ExerciseLogic
from video_engine.reporting import AnalysisReport, RepDetail

class ExerciseAnalyzer:
    """The core engine that processes video and generates an analysis."""
    def __init__(self, exercise_logic: ExerciseLogic):
        self.logic = exercise_logic
        self.pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def _extract_data(self, video_path: str):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened(): raise IOError(f"Could not open video file: {video_path}")
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        angle_timeseries, form_feedback = [], set()
        rep_state = 'up'

        print(f"Starting Pass 1: Fast Data Extraction...")
        for frame_idx in range(total_frames):
            ret, frame = cap.read()
            if not ret: break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(image)
            
            current_angle = None
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                current_angle = self.logic.get_main_angle(landmarks, frame.shape)
                angle_timeseries.append(current_angle)
                
                # Update rep state based on angle for contextual feedback
                if current_angle is not None:
                    if current_angle < 100: rep_state = 'down'
                    if current_angle > 150: rep_state = 'up'
                
                # Pass the current state to the form checker
                form_feedback.update(self.logic.get_form_feedback(landmarks, frame.shape, rep_state))
            else:
                angle_timeseries.append(None)
            
            if (frame_idx + 1) % 30 == 0:
                print(f"Progress: {((frame_idx + 1) / total_frames) * 100:.2f}%", end='\r')
        
        cap.release()
        print("\nPass 1 Complete.")
        return angle_timeseries, list(form_feedback), fps, total_frames

    # ... The rest of your analysis_engine.py file remains exactly the same ...
    def _analyze_reps(self, angle_timeseries: list, fps: float) -> list:
        print("Starting Pass 2: Signal Processing and Rep Analysis...")
        angles = np.array([angle if angle is not None else 180 for angle in angle_timeseries])
        
        troughs, _ = find_peaks(-angles, prominence=20, distance=fps*0.4)
        peaks, _ = find_peaks(angles, prominence=20, distance=fps*0.4)
        
        if len(troughs) == 0: return []

        rep_details = []
        for trough_frame in troughs:
            peaks_before = peaks[peaks < trough_frame]
            peaks_after = peaks[peaks > trough_frame]

            if len(peaks_before) > 0 and len(peaks_after) > 0:
                start_peak = peaks_before[-1]
                end_peak = peaks_after[0]

                min_angle = angles[trough_frame]
                time_taken = (end_peak - start_peak) / fps

                if time_taken < 0.3 or time_taken > 5.0:
                    continue

                rep_details.append(RepDetail(
                    rep_number=len(rep_details) + 1,
                    time_taken=round(time_taken, 2),
                    min_angle=round(min_angle, 2),
                ))
        
        print("Pass 2 Complete.")
        return rep_details

    def process_video(self, video_path: str) -> AnalysisReport:
        angle_data, form_feedback, fps, total_frames = self._extract_data(video_path)
        rep_details = self._analyze_reps(angle_data, fps)
        workout_duration = total_frames / fps
        
        return AnalysisReport(
            exercise_type=self.logic.__class__.__name__.replace('Logic', ''),
            total_repetitions=len(rep_details),
            workout_duration_sec=round(workout_duration, 2),
            average_pace_reps_per_sec=round(len(rep_details) / workout_duration, 2) if workout_duration > 0 else 0,
            form_feedback=sorted(form_feedback),
            rep_details=rep_details
        )