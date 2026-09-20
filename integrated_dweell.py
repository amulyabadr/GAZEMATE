import time
import pyautogui


class DwellClick:

    def __init__(
        self,
        dwell_time=2.0,
        movement_threshold=0.08
    ):

        self.dwell_time = dwell_time
        self.movement_threshold = movement_threshold

        self.last_x = None
        self.last_y = None

        self.start_time = None

        self.clicked = False

    def update(self, x, y):

        # First position
        if self.last_x is None:

            self.last_x = x
            self.last_y = y

            self.start_time = time.time()

            self.clicked = False

            return False

        # Calculate movement
        distance = (
            (x - self.last_x) ** 2
            + (y - self.last_y) ** 2
        ) ** 0.5

        # Update position even for small movements
        self.last_x = x
        self.last_y = y

        # If gaze moved significantly,
        # restart the dwell timer
        if distance > self.movement_threshold:

            self.start_time = time.time()

            self.clicked = False

            return False

        # Check dwell time
        elapsed_time = (
            time.time() - self.start_time
        )

        if (
            elapsed_time >= self.dwell_time
            and not self.clicked
        ):

            pyautogui.click()

            self.clicked = True

            print("Dwell click triggered.")

            return True

        return False

    def reset(self):

        self.last_x = None
        self.last_y = None

        self.start_time = None

        self.clicked = False


if __name__ == "__main__":

    print("Dwell Click Test")

    print(
        "Keep the cursor still for 2 seconds."
    )

    dwell = DwellClick(
        dwell_time=2.0
    )

    x, y = 0.5, 0.5

    for i in range(30):

        if dwell.update(x, y):

            print("Dwell click triggered.")

            break

        time.sleep(0.1)