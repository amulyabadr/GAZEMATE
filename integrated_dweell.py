import time
import pyautogui


class DwellClick:

    def __init__(
        self,
        dwell_time=3.5,
        movement_threshold=0.12
    ):

        self.dwell_time = dwell_time
        self.movement_threshold = movement_threshold

        self.last_x = None
        self.last_y = None

        self.start_time = None

        self.clicked = False

    def update(self, x, y):

        if self.last_x is None:

            self.last_x = x
            self.last_y = y

            self.start_time = time.time()

            self.clicked = False

            return False

        distance = (
            (x - self.last_x) ** 2
            + (y - self.last_y) ** 2
        ) ** 0.5

        self.last_x = x
        self.last_y = y

        if distance > self.movement_threshold:

            self.start_time = time.time()

            self.clicked = False

            return False

        elapsed_time = (
            time.time()
            - self.start_time
        )

        if (
            elapsed_time >= self.dwell_time
            and not self.clicked
        ):

            pyautogui.click()

            self.clicked = True

            print(
                "Basic dwell click triggered."
            )

            return True

        return False

    def reset(self):

        self.last_x = None
        self.last_y = None

        self.start_time = None

        self.clicked = False


if __name__ == "__main__":

    print(
        "Basic Dwell Click Test"
    )

    print(
        "Keep the cursor still for 3.5 seconds."
    )

    dwell = DwellClick()

    x, y = 0.5, 0.5

    for i in range(45):

        if dwell.update(x, y):

            print(
                "Dwell click triggered."
            )

            break

        time.sleep(0.1)