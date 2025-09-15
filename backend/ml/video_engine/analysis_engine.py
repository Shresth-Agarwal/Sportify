import cv2
import numpy as np
import mediapipe as mp
import math
import time
from scipy.signal import find_peaks

# --- Base Class for Exercise Logic (The "Plugin" Blueprint) ---
class ExerciseLogic:
    def __init__(self):
        # Thresholds and parameters specific to each exercise
        self.peak_prominence = 30  # How significant a peak must be to count
        self.peak_distance_fps_multiplier = 0.4 # Minimum distance between reps in seconds

    def get_main_angle(self, landmarks, frame_shape):
        """Must be implemented by each exercise to return the primary angle for rep counting."""
        raise NotImplementedError

    def check_form(self, landmarks, frame_shape):
        """Must be implemented by each exercise to return form feedback."""
        raise NotImplementedError

# --- Specific Exercise Implementations ---
class PushupLogic(ExerciseLogic):
    def __init__(self):
        super().__init__()

    def get_main_angle(self, landmarks, frame_shape):
        h, w, _ = frame_shape
        shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
        elbow = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.LEFT_ELBOW.value].y * h]
        wrist = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.LEFT_WRIST.value].y * h]
        return self._calculate_angle(shoulder, elbow, wrist)

    def check_form(self, landmarks, frame_shape):
        feedback = set()
        h, w, _ = frame_shape
        shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
        hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y * h]
        ankle = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y * h]
        
        body_angle = self._calculate_angle(shoulder, hip, ankle)
        if body_angle is not None and body_angle < 160:
            feedback.add("Form Issue: Keep your body straight (don't sag your hips).")
        return feedback

    def _calculate_angle(self, p1, p2, p3):
        # Angle calculation logic remains the same
        angle = math.degrees(math.atan2(p3[1] - p2[1], p3[0] - p2[0]) -
                             math.atan2(p1[1] - p2[1], p1[0] - p2[0]))
        angle = abs(angle)
        return 360 - angle if angle > 180 else angle

class SquatLogic(ExerciseLogic):
    def __init__(self):
        super().__init__()
        self.peak_prominence = 20 # Squats can have less pronounced peaks

    def get_main_angle(self, landmarks, frame_shape):
        h, w, _ = frame_shape
        hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y * h]
        knee = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].y * h]
        ankle = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.LEFT_ANKLE.value].y * h]
        return self._calculate_angle(hip, knee, ankle)

    def check_form(self, landmarks, frame_shape):
        feedback = set()
        h, w, _ = frame_shape
        shoulder = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
        hip = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.LEFT_HIP.value].y * h]
        knee = [landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.LEFT_KNEE.value].y * h]
        
        back_angle = self._calculate_angle(shoulder, hip, knee)
        if back_angle is not None and back_angle < 80:
            feedback.add("Form Issue: Keep your chest up and back straight.")
        return feedback
        
    def _calculate_angle(self, p1, p2, p3):
        angle = math.degrees(math.atan2(p3[1] - p2[1], p3[0] - p2[0]) -
                             math.atan2(p1[1] - p2[1], p1[0] - p2[0]))
        angle = abs(angle)
        return 360 - angle if angle > 180 else angle

# --- The Main Analysis Engine ---
class ExerciseAnalyzer:
    def __init__(self, exercise_logic):
        self.logic = exercise_logic
        self.pose = mp.solutions.pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def process_video_and_extract_data(self, video_path):
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened(): return None, None, None
        
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        angle_timeseries = []
        form_feedback = set()
        
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
                frame_feedback = self.logic.check_form(landmarks, frame.shape)
                form_feedback.update(frame_feedback)
            
            angle_timeseries.append(current_angle)
            if (frame_idx + 1) % 30 == 0:
                print(f"Progress: {((frame_idx + 1) / total_frames) * 100:.2f}%", end='\r')
        
        cap.release()
        print("\nPass 1 Complete.")
        return angle_timeseries, form_feedback, fps, total_frames

    def analyze_reps_from_angle_data(self, angle_timeseries, fps):
        print("Starting Pass 2: Signal Processing and Rep Analysis...")
        angles = np.array([angle if angle is not None else 180 for angle in angle_timeseries])
        
        peaks, _ = find_peaks(-angles, prominence=self.logic.peak_prominence, distance=fps*self.logic.peak_distance_fps_multiplier)
        rep_count = len(peaks)
        
        if rep_count == 0: return {"rep_count": 0, "rep_details": []}

        rep_details = []
        for i, peak_frame in enumerate(peaks):
            start_frame = peaks[i-1] if i > 0 else 0
            min_angle = np.min(angles[start_frame:peak_frame+1])
            time_taken = (peak_frame - start_frame) / fps
            rep_details.append({ "rep_number": i + 1, "time_taken": time_taken, "min_angle": min_angle })

        print("Pass 2 Complete.")
        return {"rep_count": rep_count, "rep_details": rep_details}

    def generate_report(self, analysis_results, form_feedback, workout_duration):
        rep_count = analysis_results["rep_count"]
        rep_details = analysis_results["rep_details"]

        print("\n" + "="*50)
        print("        DETAILED EXERCISE PERFORMANCE REPORT")
        print("="*50)
        print(f"\n[ Overall Performance ]")
        print(f"  - Exercise Analyzed:     {self.logic.__class__.__name__.replace('Logic', '')}")
        print(f"  - Total Repetitions:     {rep_count}")
        print(f"  - Workout Duration:      {workout_duration:.2f} seconds")
        if rep_count > 0: print(f"  - Average Pace:          {rep_count / workout_duration:.2f} reps/second")
        
        print("\n[ Qualitative Form Feedback ]")
        if not form_feedback:
            print("  - Excellent! No consistent form issues were detected.")
        else:
            for feedback in sorted(list(form_feedback)): print(f"  - {feedback}")
        
        # ... The rest of the report generation logic ...
        print("\n[ Consistency & Endurance ]")
        if len(rep_details) > 1:
            all_rep_times = [rep['time_taken'] for rep in rep_details]
            avg_rep_time = np.mean(all_rep_times)
            fastest_rep, slowest_rep = min(all_rep_times), max(all_rep_times)
            
            first_half = all_rep_times[:len(all_rep_times)//2]
            second_half = all_rep_times[len(all_rep_times)//2:]
            if first_half and second_half:
                avg_first_half_speed = np.mean(first_half)
                avg_second_half_speed = np.mean(second_half)
                speed_change = ((avg_second_half_speed - avg_first_half_speed) / avg_first_half_speed) * 100
                print(f"  - Average Time Per Rep:  {avg_rep_time:.2f} seconds")
                print(f"  - Fastest Rep:           {fastest_rep:.2f} seconds")
                print(f"  - Slowest Rep:           {slowest_rep:.2f} seconds")
                if speed_change > 0:
                    print(f"  - Performance Drop-off:  Reps slowed by {speed_change:.1f}% in the second half.")
                else:
                    print(f"  - Strong Finish:         Reps sped up by {-speed_change:.1f}% in the second half.")
        else: print("  - Not enough data for consistency analysis.")
        
        print("\n[ Form & Range of Motion (ROM) ]")
        if len(rep_details) > 0:
            all_angles = [rep['min_angle'] for rep in rep_details]
            avg_depth, best_depth, worst_depth = np.mean(all_angles), min(all_angles), max(all_angles)
            print(f"  - Avg. Rep Depth (Angle): {avg_depth:.2f}°")
            print(f"  - Deepest Rep (Min Angle):      {best_depth:.2f}°")
            print(f"  - Shallowest Rep (Max Angle):   {worst_depth:.2f}°")
        else: print("  - No completed reps to analyze for ROM.")
        print("="*50)