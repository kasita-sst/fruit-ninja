import mediapipe as mp
import cv2

class HandTracker:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands = 2,
            min_detection_confidence = 0.7,
            min_tracking_confidence = 0.5
        )

        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 800)
        self.cap.set(4, 320)

    def process_frame(self):
        success, img = self.cap.read()
        if not success:
            print("Failed to read camera frame")
            return False, None

        img = cv2.flip(img, 1)
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb)

        return True, img, results

    def release_camera(self):
        self.cap.release()
        