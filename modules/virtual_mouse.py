import cv2
import numpy as np
import pyautogui
import math
import time


class VirtualMouse:

    def __init__(self):

        # Screen Size
        self.screen_w, self.screen_h = pyautogui.size()

        # Webcam Resolution
        self.cam_w = 1280
        self.cam_h = 720

        # Frame Reduction Area
        self.frameR = 100

        # Smoothening
        self.smoothening = 7

        self.plocX = 0
        self.plocY = 0

        self.clocX = 0
        self.clocY = 0

        # Click Delay
        self.last_click = 0
        self.click_delay = 0.35

        pyautogui.FAILSAFE = False

    def process(self, frame, lmList, fingers):

        if len(lmList) == 0:
            return frame

        # Index Finger Tip
        x1, y1 = lmList[8][1], lmList[8][2]

        # Middle Finger Tip
        x2, y2 = lmList[12][1], lmList[12][2]

        h, w, _ = frame.shape

        # Draw Active Region
        cv2.rectangle(
            frame,
            (self.frameR, self.frameR),
            (w - self.frameR, h - self.frameR),
            (255, 0, 255),
            2,
        )

        # ------------------------------------------------
        # MOVE MODE
        # Only Index Finger Up
        # ------------------------------------------------

        if fingers == [0, 1, 0, 0, 0]:

            cv2.circle(frame, (x1, y1), 12, (0, 255, 0), cv2.FILLED)

            # Convert Camera Coordinates to Screen Coordinates

            x3 = np.interp(
                x1,
                (self.frameR, w - self.frameR),
                (0, self.screen_w),
            )

            y3 = np.interp(
                y1,
                (self.frameR, h - self.frameR),
                (0, self.screen_h),
            )

            # Smooth Cursor

            self.clocX = self.plocX + (x3 - self.plocX) / self.smoothening
            self.clocY = self.plocY + (y3 - self.plocY) / self.smoothening

            pyautogui.moveTo(
                self.screen_w - self.clocX,
                self.clocY,
            )

            self.plocX = self.clocX
            self.plocY = self.clocY

            cv2.putText(
                frame,
                "MOVE",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

        # ------------------------------------------------
        # CLICK MODE
        # Index + Middle Finger Up
        # ------------------------------------------------

        elif fingers == [0, 1, 1, 0, 0]:

            length = math.hypot(x2 - x1, y2 - y1)

            cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 2)

            cv2.circle(frame, (x1, y1), 8, (0, 255, 255), cv2.FILLED)
            cv2.circle(frame, (x2, y2), 8, (0, 255, 255), cv2.FILLED)

            cv2.putText(
                frame,
                f"Distance : {int(length)}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2,
            )

            if (
                length < 35
                and time.time() - self.last_click > self.click_delay
            ):

                pyautogui.click()

                self.last_click = time.time()

                cv2.circle(
                    frame,
                    ((x1 + x2) // 2, (y1 + y2) // 2),
                    15,
                    (0, 255, 0),
                    cv2.FILLED,
                )

                cv2.putText(
                    frame,
                    "CLICK",
                    (20, 40),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 0),
                    2,
                )

        return frame