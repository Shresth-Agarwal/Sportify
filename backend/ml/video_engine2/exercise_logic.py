import mediapipe as mp
import numpy as np

class ExerciseLogic:
    """Base class defining the contract for an exercise's logic."""
    def get_main_angle(self, landmarks, frame_shape):
        """Must return the primary angle for rep counting."""
        raise NotImplementedError

    def get_form_feedback(self, landmarks, frame_shape, rep_state):
        """Must return a set of form feedback strings."""
        raise NotImplementedError
        
    def _calculate_angle(self, p1, p2, p3):
        """Calculates a stable angle from three landmark points using vector math."""
        p1, p2, p3 = np.array(p1), np.array(p2), np.array(p3)
        v1 = p1 - p2
        v2 = p3 - p2
        dot_product = np.dot(v1, v2)
        norm_product = np.linalg.norm(v1) * np.linalg.norm(v2)
        if norm_product == 0: return None
        cosine_angle = dot_product / np.clip(norm_product, 1e-7, np.inf)
        angle = np.degrees(np.arccos(np.clip(cosine_angle, -1.0, 1.0)))
        return angle

class PushupLogic(ExerciseLogic):
    """Contains all specific logic for analyzing a push-up."""
    def get_main_angle(self, landmarks, frame_shape):
        h, w, _ = frame_shape
        # We use the RIGHT side as it's more likely to be visible in typical camera setups.
        shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
        elbow = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].y * h]
        wrist = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].y * h]
        return self._calculate_angle(shoulder, elbow, wrist)

    def get_form_feedback(self, landmarks, frame_shape, rep_state):
        feedback = set()
        h, w, _ = frame_shape
        
        # Get all necessary landmarks
        r_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
        r_hip = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].y * h]
        r_ankle = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].y * h]
        r_ear = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_EAR.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_EAR.value].y * h]
        
        # Check 1: Body Alignment (Sagging Hips)
        body_angle = self._calculate_angle(r_shoulder, r_hip, r_ankle)
        if body_angle is not None and body_angle < 160:
            feedback.add("Form Issue: Keep your body straight (don't sag your hips).")
            
        # Check 2: Elbow Angle at Bottom (Depth)
        if rep_state == 'down':
            elbow_angle = self.get_main_angle(landmarks, frame_shape)
            if elbow_angle is not None and elbow_angle > 95:
                feedback.add("Form Issue: Go lower for full range of motion (elbows should be around 90° or less).")

        # Check 3: Head Position
        head_angle = self._calculate_angle(r_ear, r_shoulder, r_hip)
        if head_angle is not None and (head_angle < 160 or head_angle > 200): # Allow 20 deg deviation
             feedback.add("Form Issue: Keep your neck aligned with your spine (don't crane your head up or down).")
        
        return feedback

class SquatLogic(ExerciseLogic):
    """Contains all specific logic for analyzing a squat."""
    def get_main_angle(self, landmarks, frame_shape):
        h, w, _ = frame_shape
        hip = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].y * h]
        knee = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value].y * h]
        ankle = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].y * h]
        return self._calculate_angle(hip, knee, ankle)

    def get_form_feedback(self, landmarks, frame_shape, rep_state):
        feedback = set()
        h, w, _ = frame_shape

        # Get all necessary landmarks for a side-on squat view
        r_hip = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].y * h]
        r_knee = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value].y * h]
        r_ankle = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].y * h]
        r_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
        r_toe = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y * h]
        r_heel = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HEEL.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HEEL.value].y * h]

        # We only check form at the bottom of the movement for squats
        if rep_state == 'down':
            # Check 1: Knee Position (Knees not past toes)
            # This assumes a side view where X is the depth axis
            if r_knee[0] > r_toe[0]:
                feedback.add("Form Issue: Avoid letting knees extend beyond toes during the descent.")
            
            # Check 2: Back Alignment (Chest up)
            back_angle = self._calculate_angle(r_shoulder, r_hip, r_knee)
            if back_angle is not None and back_angle < 80:
                feedback.add("Form Issue: Keep your chest up and back straight (avoid rounding the spine).")

            # Check 3: Depth of Squat (Hip crease below knees)
            # In image coordinates, a higher Y value is lower on the screen.
            if r_hip[1] < r_knee[1]:
                feedback.add("Form Issue: Squat deeper to improve effectiveness (hip crease should go lower).")
        
        # Check 4: Foot Placement (Heel lift) - checked throughout
        # Check if the heel's y-coordinate is significantly higher than the ankle's
        if abs(r_heel[1] - r_ankle[1]) > 20: # Threshold of 20 pixels
            feedback.add("Form Issue: Keep feet flat on the ground for better stability.")

        return feedback