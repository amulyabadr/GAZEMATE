import cv2
import mediapipe as mp
import threading
import tkinter as tk

from integrated_eye_detection import detect_face_and_eyes
from integrated_gaze import estimate_gaze
from integrated_cursor import CursorController
from integrated_dweell import DwellClick
from integrated_calibration import GazeCalibration
from integrated_keyboard import AccessibleVirtualKeyboard


class GazeMate:

    def __init__(self):

        self.running = True

        self.calibration = GazeCalibration()

        self.cursor = CursorController()

        self.dwell = DwellClick(
            dwell_time=2.0
        )

        self.keyboard = None

    def eye_tracking(self):

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():

            print("Could not open webcam.")

            self.running = False

            return

        mp_face_mesh = mp.solutions.face_mesh

        with mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:

            while self.running:

                success, frame = camera.read()

                if not success:
                    continue

                frame = cv2.flip(frame, 1)

                (
                    frame,
                    face_detected,
                    left_eye_detected,
                    right_eye_detected,
                    iris_detected,
                    landmarks
                ) = detect_face_and_eyes(
                    frame,
                    face_mesh
                )

                if (
                    face_detected
                    and iris_detected
                    and landmarks is not None
                ):

                    gaze = estimate_gaze(
                        landmarks[0].landmark,
                        frame.shape[1],
                        frame.shape[0]
                    )

                    if gaze is not None:

                        gaze_x, gaze_y = gaze

                        screen_position = (
                            self.calibration.map_gaze(
                                gaze_x,
                                gaze_y
                            )
                        )

                        if screen_position is not None:

                            screen_x, screen_y = screen_position

                            print(
                                f"Cursor: "
                                f"{screen_x:.2f}, "
                                f"{screen_y:.2f}"
                            )

                            self.cursor.move_cursor(
                                screen_x,
                                screen_y
                            )

                            self.dwell.update(
                                screen_x,
                                screen_y
                            )

                cv2.imshow(
                    "GazeMate Eye Tracking",
                    frame
                )

                if cv2.waitKey(1) & 0xFF == ord("q"):

                    self.running = False

        camera.release()
        cv2.destroyAllWindows()

    def start(self):

        print("Starting GazeMate...")

        print("Starting calibration...")

        if not self.calibration.calibrate():

            print("Calibration failed.")

            return

        print("Calibration completed.")

        print("Opening virtual keyboard...")

        self.keyboard = AccessibleVirtualKeyboard()

        tracking_thread = threading.Thread(
            target=self.eye_tracking,
            daemon=True
        )

        tracking_thread.start()

        self.keyboard.mainloop()

        self.running = False


if __name__ == "__main__":

    app = GazeMate()

    app.start()