import cv2

from gesture import GestureEngine


class VideoCamera:

    def __init__(self):

        self.cap = cv2.VideoCapture(0)

        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        self.engine = GestureEngine()

    def __del__(self):

        self.cap.release()

    def get_frame(self):

        success, frame = self.cap.read()

        if not success:
            return None

        frame = cv2.flip(frame, 1)

        frame, gesture, fingers = self.engine.process(frame)

        ret, buffer = cv2.imencode(".jpg", frame)

        return buffer.tobytes()