import pyautogui


class CursorController:

    def __init__(self, smoothing=0.25):

        self.smoothing = smoothing

        self.current_x = 0.5
        self.current_y = 0.5

        self.screen_width, self.screen_height = pyautogui.size()

    def move_cursor(self, x, y):

        # Keep cursor away from screen edges
        x = max(0.02, min(0.98, x))
        y = max(0.02, min(0.98, y))

        # Smooth cursor movement

        self.current_x = (
            self.current_x
            + self.smoothing * (x - self.current_x)
        )

        self.current_y = (
            self.current_y
            + self.smoothing * (y - self.current_y)
        )

        # Convert normalized coordinates
        # to screen coordinates

        screen_x = int(
            self.current_x * (self.screen_width - 1)
        )

        screen_y = int(
            self.current_y * (self.screen_height - 1)
        )

        # Keep actual mouse position away from corners

        screen_x = max(
            10,
            min(self.screen_width - 10, screen_x)
        )

        screen_y = max(
            10,
            min(self.screen_height - 10, screen_y)
        )

        pyautogui.moveTo(
            screen_x,
            screen_y,
            duration=0
        )


if __name__ == "__main__":

    print("Cursor Controller Test")

    controller = CursorController()

    controller.move_cursor(0.5, 0.5)

    print("Cursor moved to screen center.")
    