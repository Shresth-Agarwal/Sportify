import cv2
import numpy as np
import mediapipe as mp
from scipy.signal import find_peaks
from video_engine.exercise_logic import ExerciseLogic
from video_engine.reporting import AnalysisReport

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
        if fps == 0: fps = 30 # Default FPS if not available

        angle_timeseries, form_feedback = [], set()
        rep_state = 'up'

        print("Starting Pass 1: Fast Data Extraction...")
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

                if current_angle is not None:
                    if current_angle < 100: rep_state = 'down'
                    if current_angle > 150: rep_state = 'up'

                form_feedback.update(self.logic.get_form_feedback(landmarks, frame.shape, rep_state))
            else:
                angle_timeseries.append(None)

            if (frame_idx + 1) % 30 == 0:
                print(f"Progress: {((frame_idx + 1) / total_frames) * 100:.2f}%", end='\r')

        cap.release()
        print("\nPass 1 Complete.")
        return angle_timeseries, list(form_feedback), fps, total_frames

    def _analyze_reps(self, angle_timeseries: list, fps: float):
        print("Starting Pass 2: Signal Processing and Rep Analysis...")
        # Replace None with a neutral angle (e.g., 180) for processing
        angles = np.array([angle if angle is not None else 180 for angle in angle_timeseries])
        
        # More robust peak detection
        troughs, _ = find_peaks(-angles, prominence=30, distance=fps*0.5)
        
        if len(troughs) == 0: return [], [], []

        rep_times, min_angles = [], []
        for i in range(len(troughs)):
            start_frame, end_frame = 0, len(angles) -1
            if i > 0: start_frame = troughs[i-1]
            if i < len(troughs) -1: end_frame = troughs[i+1]

            # Find the peaks (highest angle) before and after the trough
            peaks_before, _ = find_peaks(angles[start_frame:troughs[i]], prominence=30)
            peaks_after, _ = find_peaks(angles[troughs[i]:end_frame], prominence=30)

            if peaks_before.size > 0 and peaks_after.size > 0:
                start_peak = start_frame + peaks_before[-1]
                end_peak = troughs[i] + peaks_after[0]
                
                time_taken = (end_peak - start_peak) / fps
                # Filter out reps that are too fast or too slow
                if 0.4 < time_taken < 5.0:
                    rep_times.append(time_taken)
                    min_angles.append(angles[troughs[i]])

        print("Pass 2 Complete.")
        return rep_times, min_angles

    def _get_workout_intensity(self, avg_rep_time: float) -> str:
        if avg_rep_time == 0: return 'N/A'
        if avg_rep_time > 3.0: return 'Low'
        if avg_rep_time > 1.5: return 'Moderate'
        return 'High'
    
    def process_video(self, video_path: str) -> AnalysisReport:
        angle_data, form_feedback, fps, total_frames = self._extract_data(video_path)
        rep_times, min_angles = self._analyze_reps(angle_data, fps)
        
        total_reps = len(rep_times)
        workout_duration = total_frames / fps
        avg_rep_time = round(np.mean(rep_times), 2) if total_reps > 0 else 0
        min_angle_range = (round(np.min(min_angles), 2), round(np.max(min_angles), 2)) if total_reps > 0 else (0,0)
        
        if total_reps == 0:
            form_feedback.append("No valid reps were detected. This could mean the wrong exercise was selected, or the camera angle makes it difficult to see your form.")

        return AnalysisReport(
            exercise_type=self.logic.__class__.__name__.replace('Logic', ''),
            total_repetitions=total_reps,
            workout_duration_sec=round(workout_duration, 2),
            average_rep_time=avg_rep_time,
            min_angle_range=min_angle_range,
            workout_intensity=self._get_workout_intensity(avg_rep_time),
            form_feedback=sorted(form_feedback)
        )