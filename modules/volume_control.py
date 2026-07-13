import cv2
import math
import numpy as np

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class VolumeControl:

    def __init__(self):

        devices = AudioUtilities.GetSpeakers()

        interface = devices.Activate(
            IAudioEndpointVolume._iid_,
            CLSCTX_ALL,
            None
        )

        self.volume = cast(
            interface,
            POINTER(IAudioEndpointVolume)
        )

        self.minVol, self.maxVol = self.volume.GetVolumeRange()[:2]

    def process(self, frame, lmList):

        if len(lmList) == 0:
            return frame

        x1, y1 = lmList[4][1], lmList[4][2]      # Thumb Tip
        x2, y2 = lmList[8][1], lmList[8][2]      # Index Tip

        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        cv2.circle(frame, (x1, y1), 10, (255, 0, 255), cv2.FILLED)
        cv2.circle(frame, (x2, y2), 10, (255, 0, 255), cv2.FILLED)

        cv2.line(frame, (x1, y1), (x2, y2), (255, 255, 0), 3)

        cv2.circle(frame, (cx, cy), 8, (0, 255, 255), cv2.FILLED)

        length = math.hypot(x2 - x1, y2 - y1)

        # Distance 20 -> 220
        vol = np.interp(
            length,
            [20, 220],
            [self.minVol, self.maxVol]
        )

        volBar = np.interp(
            length,
            [20, 220],
            [400, 150]
        )

        volPer = np.interp(
            length,
            [20, 220],
            [0, 100]
        )

        self.volume.SetMasterVolumeLevel(vol, None)

        # Volume Bar

        cv2.rectangle(
            frame,
            (50, 150),
            (85, 400),
            (255, 255, 255),
            3
        )

        cv2.rectangle(
            frame,
            (50, int(volBar)),
            (85, 400),
            (0, 255, 0),
            cv2.FILLED
        )

        cv2.putText(
            frame,
            f"{int(volPer)}%",
            (35, 440),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "VOLUME",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (0, 255, 255),
            2
        )

        return frame