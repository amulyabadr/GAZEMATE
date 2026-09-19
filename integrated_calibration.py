import cv2
import mediapipe as mp
import numpy as np
import pyautogui
import json
import os
import time

from integrated_gaze import estimate_gaze


class GazeCalibration:

    def __init__(self):

        self.screen_width, self.screen_height = (
            pyautogui.size()
        )

        self.save_path = (
            "calibration_data/calibration_data.json"
        )

        # Reduced calibration points
        self.points = [

            (0.20, 0.20),

            (0.50, 0.50),

            (0.80, 0.80)

        ]

        self.mapping_x = None
        self.mapping_y = None

    def calibrate(self):

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():

            print(
                "Could not open webcam."
            )

            return False

        mp_face_mesh = mp.solutions.face_mesh

        window_name = (
            "GazeMate Basic Calibration"
        )

        cv2.namedWindow(
            window_name,
            cv2.WINDOW_NORMAL
        )

        cv2.setWindowProperty(
            window_name,
            cv2.WND_PROP_FULLSCREEN,
            cv2.WINDOW_FULLSCREEN
        )

        gaze_samples = []
        screen_points = []

        with mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.6
        ) as face_mesh:

            for point in self.points:

                target_x = int(
                    point[0]
                    * self.screen_width
                )

                target_y = int(
                    point[1]
                    * self.screen_height
                )

                samples = []

                start_time = time.time()

                # Shorter sampling time
                while (
                    time.time()
                    - start_time
                    < 2
                ):

                    success, frame = (
                        camera.read()
                    )

                    if not success:
                        continue

                    frame = cv2.flip(
                        frame,
                        1
                    )

                    rgb = cv2.cvtColor(
                        frame,
                        cv2.COLOR_BGR2RGB
                    )

                    results = (
                        face_mesh.process(rgb)
                    )

                    display = np.zeros(
                        (
                            self.screen_height,
                            self.screen_width,
                            3
                        ),
                        dtype=np.uint8
                    )

                    cv2.circle(
                        display,
                        (target_x, target_y),
                        15,
                        (0, 255, 255),
                        -1
                    )

                    cv2.putText(
                        display,
                        "Look at the circle",
                        (50, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        2
                    )

                    if results.multi_face_landmarks:

                        landmarks = (
                            results
                            .multi_face_landmarks[0]
                            .landmark
                        )

                        gaze = estimate_gaze(
                            landmarks,
                            frame.shape[1],
                            frame.shape[0]
                        )

                        if gaze is not None:

                            # Reduce stored precision
                            gaze_x = round(
                                gaze[0],
                                1
                            )

                            gaze_y = round(
                                gaze[1],
                                1
                            )

                            samples.append(
                                (gaze_x, gaze_y)
                            )

                    cv2.imshow(
                        window_name,
                        display
                    )

                    if (
                        cv2.waitKey(1)
                        & 0xFF
                        == 27
                    ):

                        camera.release()

                        cv2.destroyAllWindows()

                        return False

                if samples:

                    average_x = np.mean(
                        [
                            sample[0]
                            for sample in samples
                        ]
                    )

                    average_y = np.mean(
                        [
                            sample[1]
                            for sample in samples
                        ]
                    )

                    gaze_samples.append(
                        (
                            average_x,
                            average_y
                        )
                    )

                    screen_points.append(
                        point
                    )

        camera.release()

        cv2.destroyAllWindows()

        if len(gaze_samples) < 3:

            print(
                "Calibration failed."
            )

            return False

        gaze_matrix = np.array(
            [
                [x, y, 1]
                for x, y in gaze_samples
            ]
        )

        screen_x = np.array(
            [
                point[0]
                for point in screen_points
            ]
        )

        screen_y = np.array(
            [
                point[1]
                for point in screen_points
            ]
        )

        self.mapping_x = np.linalg.lstsq(
            gaze_matrix,
            screen_x,
            rcond=None
        )[0]

        self.mapping_y = np.linalg.lstsq(
            gaze_matrix,
            screen_y,
            rcond=None
        )[0]

        os.makedirs(
            "calibration_data",
            exist_ok=True
        )

        data = {

            "mapping_x":
                self.mapping_x.tolist(),

            "mapping_y":
                self.mapping_y.tolist()

        }

        with open(
            self.save_path,
            "w"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

        print(
            "Basic calibration completed."
        )

        return True

    def map_gaze(
        self,
        gaze_x,
        gaze_y
    ):

        if (
            self.mapping_x is None
            or self.mapping_y is None
        ):

            return None

        values = np.array(
            [
                gaze_x,
                gaze_y,
                1
            ]
        )

        screen_x = np.dot(
            values,
            self.mapping_x
        )

        screen_y = np.dot(
            values,
            self.mapping_y
        )

        screen_x = max(
            0,
            min(1, screen_x)
        )

        screen_y = max(
            0,
            min(1, screen_y)
        )

        return (
            screen_x,
            screen_y
        )
if __name__ == "__main__":
    calibration = GazeCalibration()
    result = calibration.calibrate()
    print("Calibration result:", result)