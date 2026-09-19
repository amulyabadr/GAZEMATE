import pyautogui


class CursorController:

    def __init__(self, smoothing=0.1):

        self.smoothing = smoothing
        self.current_x = None
        self.current_y = None

    def move_cursor(self, x, y):

        screen_width, screen_height = pyautogui.size()

        target_x = x * screen_width
        target_y = y * screen_height

        if self.current_x is None:

            self.current_x = target_x
            self.current_y = target_y

        else:

            self.current_x += self.smoothing * (
                target_x - self.current_x
            )

            self.current_y += self.smoothing * (
                target_y - self.current_y
            )

        pyautogui.moveTo(
            int(self.current_x),
            int(self.current_y)
        )