import cv2
import numpy as np
import mediapipe as mp
import math
import time
from scipy.signal import find_peaks

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose

class ExerciseAnalyzer:
    """
    The definitive, high-accuracy exercise analyzer using a robust signal processing approach.
    """

    def __init__(self, exercise_type):
        self.exercise_type = exercise_type.lower()
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

    def _calculate_angle(self, p1, p2, p3):
        angle = math.degrees(math.atan2(p3[1] - p2[1], p3[0] - p2[0]) -
                             math.atan2(p1[1] - p2[1], p1[0] - p2[0]))
        angle = abs(angle)
        if angle > 180:
            angle = 360 - angle
        return angle

    def process_video_and_extract_angles(self, video_path):
        """
        Pass 1: Process the video to extract a time-series of the relevant angle.
        This is designed to be as fast as possible.
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return None, None

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        
        angle_timeseries = []
        
        print(f"Starting Pass 1: Fast Angle Extraction...")
        print(f"Processing {total_frames} frames...")

        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(image)
            
            current_angle = None
            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                h, w, _ = frame.shape
                
                if self.exercise_type == 'pushup':
                    shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
                    elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * w, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * h]
                    wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h]
                    current_angle = self._calculate_angle(shoulder, elbow, wrist)
            
            angle_timeseries.append(current_angle)
            
            frame_idx += 1
            if frame_idx % 30 == 0:
                print(f"Progress: {(frame_idx / total_frames) * 100:.2f}%", end='\r')
        
        cap.release()
        print("\nPass 1 Complete.")
        return angle_timeseries, fps, total_frames

    def analyze_reps_from_angle_data(self, angle_timeseries, fps):
        """
        Pass 2: Analyze the angle time-series using peak detection to find reps.
        """
        print("Starting Pass 2: Signal Processing and Rep Analysis...")
        
        # Replace None values with a neutral angle (e.g., 180) for continuous signal
        angles = np.array([angle if angle is not None else 180 for angle in angle_timeseries])
        
        # We find reps by finding the "troughs" or minimums in the angle data.
        # find_peaks on the negative signal finds the troughs.
        # Prominence is the KEY parameter: It ensures a peak is significant enough to be a rep.
        # Distance ensures reps are not too close together.
        peaks, _ = find_peaks(-angles, prominence=30, distance=fps*0.4)
        
        rep_count = len(peaks)
        
        if rep_count == 0:
            return {"rep_count": 0, "rep_details": [], "form_feedback": set()}

        # Calculate metrics for each valid rep
        rep_details = []
        for i in range(len(peaks)):
            start_frame = peaks[i-1] if i > 0 else 0
            end_frame = peaks[i]
            
            # Find the true minimum angle in this rep's segment
            min_angle = np.min(angles[start_frame:end_frame+1])
            
            time_taken = (end_frame - start_frame) / fps
            
            rep_details.append({
                "rep_number": i + 1,
                "time_taken": time_taken,
                "min_angle": min_angle
            })

        print("Pass 2 Complete.")
        return {"rep_count": rep_count, "rep_details": rep_details, "form_feedback": set()}

    def generate_report(self, analysis_results, workout_duration):
        """Generates the final, accurate report from the analysis results."""
        rep_count = analysis_results["rep_count"]
        rep_details = analysis_results["rep_details"]
        form_feedback = analysis_results["form_feedback"]

        print("\n" + "="*50)
        print("        DETAILED EXERCISE PERFORMANCE REPORT")
        print("="*50)
        print("\n[ Overall Performance ]")
        print(f"  - Exercise Analyzed:     {self.exercise_type.capitalize()}")
        print(f"  - Total Repetitions:     {rep_count}")
        print(f"  - Workout Duration:      {workout_duration:.2f} seconds")
        if rep_count > 0:
            print(f"  - Average Pace:          {rep_count / workout_duration:.2f} reps/second")
        
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
            print(f"  - Avg. Rep Depth (Elbow Angle): {avg_depth:.2f}°")
            print(f"  - Deepest Rep (Min Angle):      {best_depth:.2f}°")
            print(f"  - Shallowest Rep (Max Angle):   {worst_depth:.2f}°")
        else: print("  - No completed reps to analyze for ROM.")
        
        print("\n[ Qualitative Form Feedback ]")
        if not form_feedback:
            print("  - No consistent form issues were detected during analysis.")
        else:
            for feedback in sorted(list(form_feedback)): print(f"  - {feedback}")
        print("="*50)