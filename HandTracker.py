import pygame
import pygame.camera

import mediapipe as mp
import numpy as np


class HandTracker:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )

        self.mp_draw = mp.solutions.drawing_utils
        
        pygame.camera.init()

        cam_list = pygame.camera.list_cameras()
        if not cam_list:
            raise RuntimeError("No camera detected!")

        self.cam = pygame.camera.Camera(cam_list[0], (800, 500))
        self.last_valid_surface = None


    def start_camera(self):
        self.cam.start()

    def process_frame(self):
        if not self.cam.query_image():
            return self.last_valid_surface, None

        raw_snapshot = self.cam.get_image()
        self.last_valid_surface = raw_snapshot


        cam_width = raw_snapshot.get_width()
        cam_height = raw_snapshot.get_height()

        #conversion
        pixel_bytes = pygame.image.tobytes(raw_snapshot, "RGB")
        img_array = np.frombuffer(pixel_bytes, dtype=np.uint8)
        img_np = img_array.reshape((cam_height, cam_width, 3)).copy()

        results = self.hands.process(img_np)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(
					img_np, 
					hand_landmarks,
                    mp.solutions.hands.HAND_CONNECTIONS
				)

        drawn_surface = pygame.image.frombuffer(img_np.tobytes(), (cam_width, cam_height), "RGB")
        
        self.last_valid_surface = drawn_surface

        return drawn_surface, results


    def release_camera(self):
        self.cam.stop()
        self.last_valid_surface = None
    
