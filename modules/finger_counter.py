class FingerCounter:

    # Thumb, Index, Middle, Ring, Pinky
    tipIds = [4, 8, 12, 16, 20]

    def count(self, lmList):

        fingers = []

        if len(lmList) == 0:
            return 0, fingers

        # Thumb
        if lmList[self.tipIds[0]][1] > lmList[self.tipIds[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # Other fingers
        for id in range(1, 5):

            if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        total = fingers.count(1)

        return total, fingers