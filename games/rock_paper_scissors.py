import cv2
import random
import time


class RockPaperScissors:

    def __init__(self):

        self.player_score = 0
        self.ai_score = 0
        self.draw_score = 0

        self.player_move = ""
        self.ai_move = ""
        self.result = ""

        self.last_time = time.time()
        self.round_delay = 3
        self.played = False

    # -------------------------------------------------

    def gesture_to_move(self, gesture):

        if gesture == "FIST":
            return "ROCK"

        elif gesture == "FIVE":
            return "PAPER"

        elif gesture == "VICTORY":
            return "SCISSORS"

        return "UNKNOWN"

    # -------------------------------------------------

    def winner(self):

        if self.player_move == self.ai_move:
            self.result = "DRAW"
            self.draw_score += 1
            return

        if (
            (self.player_move == "ROCK" and self.ai_move == "SCISSORS")
            or
            (self.player_move == "PAPER" and self.ai_move == "ROCK")
            or
            (self.player_move == "SCISSORS" and self.ai_move == "PAPER")
        ):

            self.result = "YOU WIN"
            self.player_score += 1

        else:

            self.result = "AI WINS"
            self.ai_score += 1

    # -------------------------------------------------

    def process(self, frame, gesture):

        current = time.time()

        elapsed = current - self.last_time
        remaining = max(0, self.round_delay - int(elapsed))

        # ---------------- Countdown ----------------

        if remaining > 0:

            cv2.circle(frame, (640, 90), 45, (0, 255, 255), 3)

            cv2.putText(
                frame,
                str(remaining),
                (620, 105),
                cv2.FONT_HERSHEY_DUPLEX,
                2,
                (0, 255, 255),
                3,
            )

            self.played = False

        else:

            if not self.played:

                self.player_move = self.gesture_to_move(gesture)

                if self.player_move != "UNKNOWN":

                    self.ai_move = random.choice(
                        ["ROCK", "PAPER", "SCISSORS"]
                    )

                    self.winner()

                    self.played = True
                    self.last_time = current

        # ---------------- Left Panel ----------------

        cv2.rectangle(frame, (20, 20), (620, 220), (40, 40, 40), -1)

        cv2.rectangle(frame, (20, 20), (620, 220), (0, 255, 255), 2)

        cv2.putText(
            frame,
            "ROCK • PAPER • SCISSORS",
            (35, 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            "Show Fist / Open Palm / Victory",
            (40, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (180, 180, 180),
            1,
        )

        cv2.putText(
            frame,
            f"You : {self.player_move}",
            (40, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"Computer : {self.ai_move}",
            (40, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2,
        )

        # ---------------- Result ----------------

        color = (255, 255, 255)

        if self.result == "YOU WIN":
            color = (0, 255, 0)

        elif self.result == "AI WINS":
            color = (0, 0, 255)

        elif self.result == "DRAW":
            color = (0, 255, 255)

        cv2.putText(
            frame,
            self.result,
            (40, 205),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            color,
            3,
        )

        # ---------------- Score Panel ----------------

        cv2.rectangle(frame, (930, 20), (1260, 185), (35, 35, 35), -1)

        cv2.rectangle(frame, (930, 20), (1260, 185), (0, 255, 255), 2)

        cv2.putText(
            frame,
            "SCORE",
            (1030, 55),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"You : {self.player_score}",
            (950, 90),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"AI : {self.ai_score}",
            (950, 125),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2,
        )

        cv2.putText(
            frame,
            f"Draw : {self.draw_score}",
            (950, 160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            2,
        )

        return frame