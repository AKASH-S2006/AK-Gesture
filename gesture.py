import cv2

from modules.hand_detection import HandDetector
from modules.finger_counter import FingerCounter
from modules.gesture_recognition import GestureRecognizer
from modules.air_canvas import AirCanvas
from modules.virtual_mouse import VirtualMouse
from modules.volume_control import VolumeControl
from games.rock_paper_scissors import RockPaperScissors


class GestureEngine:

    def __init__(self):

        self.detector = HandDetector()

        self.counter = FingerCounter()

        self.recognizer = GestureRecognizer()

        self.canvas = AirCanvas()

        self.virtual_mouse = VirtualMouse()

        self.volume = VolumeControl()

        # Modes
        self.mode = "volume_control"

        self.rps = RockPaperScissors()


        # Available Modes
        # hand_detection
        # finger_counter
        # air_canvas
        # virtual_mouse
        # volume_control

    def process(self, frame):

        frame = self.detector.findHands(frame)

        lmList = self.detector.findPosition(frame, draw=False)

        finger_count = 0

        gesture = "NO HAND"

        if len(lmList) != 0:

            finger_count, fingers = self.counter.count(lmList)

            gesture = self.recognizer.recognize(fingers)

            # -------------------------
            # Feature Selection
            # -------------------------
            if self.mode == "air_canvas":

                frame = self.canvas.process(
                    frame,
                    lmList,
                    fingers
                )

            elif self.mode == "virtual_mouse":

                frame = self.virtual_mouse.process(
                    frame,
                    lmList,
                    fingers
                )

            elif self.mode == "volume_control":

                frame = self.volume.process(
                    frame,
                    lmList
                )

            elif self.mode == "finger_counter":

                # Only display finger count
                pass

            elif self.mode == "hand_detection":

                # Just show detected hand landmarks
                pass
            
            elif self.mode == "rps":

                frame = self.rps.process(
                    frame,
                    gesture
                )

            # -------------------------
            # HUD
            # -------------------------

            cv2.putText(
                frame,
                f"Mode : {self.mode}",
                (20,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,255),
                2
            )

            cv2.putText(
                frame,
                f"Gesture : {gesture}",
                (20,75),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2
            )

            cv2.putText(
                frame,
                f"Fingers : {finger_count}",
                (20,110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (255,255,0),
                2
            )

        return frame, gesture, finger_count