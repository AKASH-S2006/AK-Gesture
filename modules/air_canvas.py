import cv2
import numpy as np


class AirCanvas:

    def __init__(self):

        self.canvas = None

        self.color = (255, 0, 255)

        self.thickness = 10

        self.xp = 0
        self.yp = 0

    def process(self, frame, lmList, fingers):

        h, w, _ = frame.shape

        if self.canvas is None:
            self.canvas = np.zeros((h, w, 3), dtype=np.uint8)

        # -----------------------------
        # No hand detected
        # -----------------------------
        if len(lmList) == 0:
            self.xp = 0
            self.yp = 0
            return frame

        # -----------------------------
        # OPEN PALM -> CLEAR
        # -----------------------------
        if fingers == [1, 1, 1, 1, 1]:

            self.canvas = np.zeros((h, w, 3), dtype=np.uint8)

            self.xp = 0
            self.yp = 0

            cv2.putText(
                frame,
                "Canvas Cleared",
                (20, 50),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                3
            )

        # -----------------------------
        # DRAW MODE
        # Index finger only
        # -----------------------------
        elif fingers == [0, 1, 0, 0, 0]:

            x1, y1 = lmList[8][1], lmList[8][2]

            cv2.circle(frame, (x1, y1), 10, self.color, cv2.FILLED)

            if self.xp == 0 and self.yp == 0:
                self.xp = x1
                self.yp = y1

            cv2.line(
                self.canvas,
                (self.xp, self.yp),
                (x1, y1),
                self.color,
                self.thickness
            )

            self.xp = x1
            self.yp = y1

        else:

            self.xp = 0
            self.yp = 0

        # -----------------------------
        # Merge drawing with camera
        # -----------------------------
        gray = cv2.cvtColor(self.canvas, cv2.COLOR_BGR2GRAY)

        _, inv = cv2.threshold(
            gray,
            20,
            255,
            cv2.THRESH_BINARY_INV
        )

        inv = cv2.cvtColor(inv, cv2.COLOR_GRAY2BGR)

        frame = cv2.bitwise_and(frame, inv)

        frame = cv2.bitwise_or(frame, self.canvas)

        return frame