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
        shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
        elbow = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].y * h]
        wrist = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].y * h]
        return self._calculate_angle(shoulder, elbow, wrist)

    def get_form_feedback(self, landmarks, frame_shape, rep_state):
        feedback = set()
        h, w, _ = frame_shape

        r_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
        r_hip = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].y * h]
        r_ankle = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ANKLE.value].y * h]
        r_ear = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_EAR.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_EAR.value].y * h]

        body_angle = self._calculate_angle(r_shoulder, r_hip, r_ankle)
        if body_angle is not None and body_angle < 155:
            feedback.add("Form Issue: Keep your body straight to avoid sagging your hips.")

        if rep_state == 'down':
            elbow_angle = self.get_main_angle(landmarks, frame_shape)
            if elbow_angle is not None and elbow_angle > 100:
                feedback.add("Form Issue: Go lower for a full range of motion.")

        head_angle = self._calculate_angle(r_ear, r_shoulder, r_hip)
        if head_angle is not None and (head_angle < 150 or head_angle > 210):
             feedback.add("Form Issue: Keep your neck aligned with your spine.")

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

        r_hip = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_HIP.value].y * h]
        r_knee = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_KNEE.value].y * h]
        r_toe = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_FOOT_INDEX.value].y * h]
        r_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
        
        if rep_state == 'down':
            if r_knee[0] > r_toe[0] + 15: # Add a small buffer
                feedback.add("Form Issue: Avoid letting knees extend too far beyond your toes.")

            back_angle = self._calculate_angle(r_shoulder, r_hip, r_knee)
            if back_angle is not None and back_angle < 75:
                feedback.add("Form Issue: Keep your chest up and back straight.")

            if r_hip[1] < r_knee[1]:
                feedback.add("Form Issue: Squat deeper for better effectiveness.")

        return feedback

class PullupLogic(ExerciseLogic):
    """Contains all specific logic for analyzing a pull-up."""
    def get_main_angle(self, landmarks, frame_shape):
        h, w, _ = frame_shape
        shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
        elbow = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW.value].y * h]
        wrist = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_WRIST.value].y * h]
        return self._calculate_angle(shoulder, elbow, wrist)

    def get_form_feedback(self, landmarks, frame_shape, rep_state):
        feedback = set()
        h, w, _ = frame_shape

        r_ear = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_EAR.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_EAR.value].y * h]
        r_shoulder = [landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].x * w, landmarks[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]

        if rep_state == 'up':
            # Check if the chin is above the shoulder level as a proxy for the bar
            if r_ear[1] > r_shoulder[1]:
                feedback.add("Form Issue: Pull higher to bring your chin over the bar.")
        
        return feedback