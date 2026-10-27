import numpy as np

EAR_THRESH = 0.21
CLOSED_FRAMES = 2

def ear(eye):
    eye = np.array(eye, dtype=float)
    a = np.linalg.norm(eye[1] - eye[5])
    b = np.linalg.norm(eye[2] - eye[4])
    c = np.linalg.norm(eye[0] - eye[3])
    return (a + b) / (2.0 * c)

class BlinkDetector:
    def __init__(self):
        self.closed = {}
        self.blinked = set()

    def update(self, name, landmarks):
        e = (ear(landmarks["left_eye"]) + ear(landmarks["right_eye"])) / 2
        if e < EAR_THRESH:
            self.closed[name] = self.closed.get(name, 0) + 1
        else:
            if self.closed.get(name, 0) >= CLOSED_FRAMES:
                self.blinked.add(name)
            self.closed[name] = 0

    def is_live(self, name):
        return name in self.blinked