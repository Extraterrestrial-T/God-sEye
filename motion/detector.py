import time
import cv2
from collections import deque
from motion.utils import save_frame, log_event
from config.settings import default_params

class MotionResult:
    def __init__(self, detected, paths=None):
        self.detected = detected
        self.paths = paths or []

class MotionDetector:
    def __init__(self, sensitivity, cooldown, buffer_size, min_area_ratio):
        self.sensitivity = sensitivity
        self.cooldown = cooldown
        self.last_capture = 0
        self.buffer = deque(maxlen=buffer_size)
        self.min_area_ratio = min_area_ratio
        self.backSub = cv2.createBackgroundSubtractorMOG2(
            history=200,
            varThreshold=int(20 + (1 - sensitivity) * 80),
            detectShadows=False
        )
        self.min_area = None

    def check(self, frame) -> MotionResult:
        self.buffer.append(frame.copy())
        if self.min_area is None:
            h, w = frame.shape[:2]; self.min_area = int(self.min_area_ratio * w * h)

        fg = self.backSub.apply(frame)
        _, th = cv2.threshold(fg, 180, 255, cv2.THRESH_BINARY)
        clean = cv2.morphologyEx(th, cv2.MORPH_OPEN,
                                 cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3)))
        cnts,_ = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        large = [c for c in cnts if cv2.contourArea(c) > self.min_area]

        now = time.time()
        if large and now - self.last_capture > self.cooldown:
            paths = []
            # save context frames
            for i, f in enumerate(self.buffer):
                p = save_frame(f, suffix=f'_ctx{i}')
                paths.append(p)
            self.last_capture = now
            log_event(f"Motion detected, saved {len(paths)} frames")
            return MotionResult(True, paths)
        return MotionResult(False)