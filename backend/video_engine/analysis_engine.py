import cv2
import numpy as np
import mediapipe as mp
import math
import time

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

class ExerciseAnalyzer:
    """
    A robust and fast exercise analyzer using Google's MediaPipe.
    """

    def __init__(self, exercise_type):
        self.exercise_type = exercise_type.lower()
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

        # Analysis state
        self.rep_counter = 0
        self.rep_state = 'up'
        self.form_feedback = set()
        self.rep_details = []
        self.current_rep_start_time = None
        self.min_angle_in_rep = 180
        self.MIN_REP_TIME = 0.4  # Min seconds for a valid rep

    def _calculate_angle(self, p1, p2, p3):
        """Calculates angle from three landmark points."""
        if p1 is None or p2 is None or p3 is None:
            return None
        # Note: MediaPipe landmarks are normalized; this logic is for pixel coords
        angle = math.degrees(math.atan2(p3[1] - p2[1], p3[0] - p2[0]) -
                             math.atan2(p1[1] - p2[1], p1[0] - p2[0]))
        # Normalize to the range [0, 180]
        angle = abs(angle)
        if angle > 180:
            angle = 360 - angle
        return angle

    def _process_pushup(self, landmarks, frame_shape):
        """Analyzes push-up form using MediaPipe landmarks."""
        DOWN_THRESHOLD, UP_THRESHOLD = 110, 145
        
        # Get landmark coordinates in pixels
        h, w, _ = frame_shape
        shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x * w, landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y * h]
        elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x * w, landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y * h]
        wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x * w, landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y * h]
        hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * w, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * h]
        ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x * w, landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y * h]

        elbow_angle = self._calculate_angle(shoulder, elbow, wrist)
        if elbow_angle is None: return

        # Rep counting logic
        if self.rep_state == 'up' and elbow_angle < DOWN_THRESHOLD:
            self.rep_state = 'down'
            self.current_rep_start_time = time.time()
            self.min_angle_in_rep = elbow_angle
        elif self.rep_state == 'down':
            self.min_angle_in_rep = min(self.min_angle_in_rep, elbow_angle)
            if elbow_angle > UP_THRESHOLD:
                rep_time = time.time() - self.current_rep_start_time
                if rep_time > self.MIN_REP_TIME:
                    self.rep_state = 'up'
                    self.rep_counter += 1
                    self.rep_details.append({
                        "rep_number": self.rep_counter, "time_taken": rep_time, "min_angle": self.min_angle_in_rep
                    })
                else: # Glitch, reset
                    self.rep_state = 'up'

        # Form feedback logic
        body_angle = self._calculate_angle(shoulder, hip, ankle)
        if body_angle is not None and body_angle < 160:
            self.form_feedback.add("Form Issue: Hips are sagging (body not straight).")

    def process_video(self, video_path):
        """Processes a video file and generates a detailed report."""
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return None

        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        workout_duration = total_frames / fps
        start_time = time.time()
        
        print(f"Starting analysis with MediaPipe engine...")
        print(f"Video: {video_path}, Duration: {workout_duration:.2f}s, Frames: {total_frames}")

        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret: break

            # Convert the BGR image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False

            # Make detection
            results = self.pose.process(image)
            
            # Extract landmarks
            if results.pose_landmarks:
                if self.exercise_type == 'pushup':
                    self._process_pushup(results.pose_landmarks.landmark, frame.shape)
            
            frame_idx += 1
            if frame_idx % 30 == 0:
                print(f"Progress: {(frame_idx / total_frames) * 100:.2f}%", end='\r')
        
        cap.release()
        end_time = time.time()
        print(f"\nAnalysis complete in {end_time - start_time:.2f} seconds.")
        return self._generate_detailed_report(workout_duration)

    def _generate_detailed_report(self, workout_duration):
        """Generates the final performance report."""
        # This function remains the same as its logic is sound.
        print("\n" + "="*50)
        print("        DETAILED EXERCISE PERFORMANCE REPORT")
        print("="*50)
        print("\n[ Overall Performance ]")
        print(f"  - Exercise Analyzed:     {self.exercise_type.capitalize()}")
        print(f"  - Total Repetitions:     {self.rep_counter}")
        print(f"  - Workout Duration:      {workout_duration:.2f} seconds")
        if self.rep_counter > 0:
            print(f"  - Average Pace:          {self.rep_counter / workout_duration:.2f} reps/second")
        print("\n[ Consistency & Endurance ]")
        if len(self.rep_details) > 1:
            all_rep_times = [rep['time_taken'] for rep in self.rep_details]
            avg_rep_time = np.mean(all_rep_times)
            fastest_rep, slowest_rep = min(all_rep_times), max(all_rep_times)
            
            first_half_time = all_rep_times[:len(all_rep_times)//2]
            second_half_time = all_rep_times[len(all_rep_times)//2:]
            avg_first_half_speed = np.mean(first_half_time)
            avg_second_half_speed = np.mean(second_half_time)
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
        if len(self.rep_details) > 0:
            all_angles = [rep['min_angle'] for rep in self.rep_details]
            avg_depth, best_depth, worst_depth = np.mean(all_angles), min(all_angles), max(all_angles)
            print(f"  - Avg. Rep Depth (Elbow Angle): {avg_depth:.2f}°")
            print(f"  - Deepest Rep (Min Angle):      {best_depth:.2f}°")
            print(f"  - Shallowest Rep (Max Angle):   {worst_depth:.2f}°")
        else: print("  - No completed reps to analyze for ROM.")
        print("\n[ Qualitative Form Feedback ]")
        if not self.form_feedback:
            print("  - Excellent! No consistent form issues were detected.")
        else:
            for feedback in sorted(list(self.form_feedback)): print(f"  - {feedback}")
        print("="*50)