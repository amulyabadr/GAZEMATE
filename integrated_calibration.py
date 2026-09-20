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

        self.screen_width, self.screen_height = pyautogui.size()

        self.save_path = "calibration_data/calibration_data.json"

        # ----------------------------------------------------
        # 9-point calibration pattern
        # ----------------------------------------------------

        self.points = [
            (0.10, 0.10),
            (0.50, 0.10),
            (0.90, 0.10),

            (0.10, 0.50),
            (0.50, 0.50),
            (0.90, 0.50),

            (0.10, 0.90),
            (0.50, 0.90),
            (0.90, 0.90)
        ]

        self.mapping_x = None
        self.mapping_y = None

    def calibrate(self):

        camera = cv2.VideoCapture(0)

        if not camera.isOpened():

            print("Could not open webcam.")

            return False

        mp_face_mesh = mp.solutions.face_mesh

        window_name = "GazeMate Calibration"

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
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:

            # ==================================================
            # Process every calibration point
            # ==================================================

            for point_number, point in enumerate(self.points):

                target_x = int(
                    point[0] * self.screen_width
                )

                target_y = int(
                    point[1] * self.screen_height
                )

                samples = []

                # --------------------------------------------------
                # Stage 1:
                # Give the user time to move their eyes to target
                # --------------------------------------------------

                stabilization_start = time.time()

                while time.time() - stabilization_start < 0.7:

                    success, frame = camera.read()

                    if not success:
                        continue

                    frame = cv2.flip(frame, 1)

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
                        18,
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

                    cv2.putText(
                        display,
                        f"Calibration point "
                        f"{point_number + 1}/{len(self.points)}",
                        (50, 105),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2
                    )

                    cv2.imshow(
                        window_name,
                        display
                    )

                    if cv2.waitKey(1) & 0xFF == 27:

                        camera.release()
                        cv2.destroyAllWindows()

                        return False

                # --------------------------------------------------
                # Stage 2:
                # Collect stable samples
                # --------------------------------------------------

                collection_start = time.time()

                while time.time() - collection_start < 1.5:

                    success, frame = camera.read()

                    if not success:
                        continue

                    frame = cv2.flip(frame, 1)

                    rgb = cv2.cvtColor(
                        frame,
                        cv2.COLOR_BGR2RGB
                    )

                    results = face_mesh.process(rgb)

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
                        18,
                        (0, 255, 255),
                        -1
                    )

                    cv2.putText(
                        display,
                        "Keep looking at the circle",
                        (50, 60),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 255, 255),
                        2
                    )

                    cv2.putText(
                        display,
                        f"Calibration point "
                        f"{point_number + 1}/{len(self.points)}",
                        (50, 105),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.8,
                        (255, 255, 255),
                        2
                    )

                    if results.multi_face_landmarks:

                        landmarks = (
                            results.multi_face_landmarks[0].landmark
                        )

                        gaze = estimate_gaze(
                            landmarks,
                            frame.shape[1],
                            frame.shape[0]
                        )

                        if gaze is not None:

                            gaze_x, gaze_y = gaze

                            # ------------------------------------------
                            # Reject clearly invalid normalized values
                            # ------------------------------------------

                            if (
                                0.0 <= gaze_x <= 1.0
                                and
                                0.0 <= gaze_y <= 1.0
                            ):

                                samples.append(
                                    (gaze_x, gaze_y)
                                )

                    cv2.imshow(
                        window_name,
                        display
                    )

                    if cv2.waitKey(1) & 0xFF == 27:

                        camera.release()
                        cv2.destroyAllWindows()

                        return False

                # ==================================================
                # Use robust median instead of simple mean
                # ==================================================

                if len(samples) >= 10:

                    samples_array = np.array(
                        samples,
                        dtype=np.float64
                    )

                    median_x = np.median(
                        samples_array[:, 0]
                    )

                    median_y = np.median(
                        samples_array[:, 1]
                    )

                    gaze_samples.append(
                        (median_x, median_y)
                    )

                    screen_points.append(point)

                    print(
                        f"Calibration point "
                        f"{point_number + 1}: "
                        f"gaze = "
                        f"({median_x:.4f}, {median_y:.4f}), "
                        f"samples = {len(samples)}"
                    )

                else:

                    print(
                        f"Calibration point "
                        f"{point_number + 1} "
                        f"did not collect enough samples."
                    )

        camera.release()
        cv2.destroyAllWindows()

        # ======================================================
        # Verify calibration
        # ======================================================

        if len(gaze_samples) < 6:

            print(
                "Calibration failed: "
                "not enough valid calibration points."
            )

            return False

        # ======================================================
        # Build affine mapping
        #
        # screen_x = a*x + b*y + c
        # screen_y = d*x + e*y + f
        # ======================================================

        gaze_matrix = np.array(
            [
                [x, y, 1.0]
                for x, y in gaze_samples
            ],
            dtype=np.float64
        )

        screen_x = np.array(
            [
                point[0]
                for point in screen_points
            ],
            dtype=np.float64
        )

        screen_y = np.array(
            [
                point[1]
                for point in screen_points
            ],
            dtype=np.float64
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

        # ======================================================
        # Calculate calibration fitting error
        # ======================================================

        predicted_x = np.dot(
            gaze_matrix,
            self.mapping_x
        )

        predicted_y = np.dot(
            gaze_matrix,
            self.mapping_y
        )

        error_x = np.abs(
            predicted_x - screen_x
        )

        error_y = np.abs(
            predicted_y - screen_y
        )

        average_error = np.mean(
            np.sqrt(
                error_x ** 2 +
                error_y ** 2
            )
        )

        print(
            f"Calibration fitting error: "
            f"{average_error:.4f}"
        )

        # ======================================================
        # Save calibration
        # ======================================================

        os.makedirs(
            "calibration_data",
            exist_ok=True
        )

        data = {
            "mapping_x": self.mapping_x.tolist(),
            "mapping_y": self.mapping_y.tolist()
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

        print("Calibration completed.")

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
                1.0
            ],
            dtype=np.float64
        )

        screen_x = np.dot(
            values,
            self.mapping_x
        )

        screen_y = np.dot(
            values,
            self.mapping_y
        )

        # ------------------------------------------------------
        # Keep normalized screen coordinates inside the screen
        # ------------------------------------------------------

        screen_x = max(
            0.0,
            min(1.0, screen_x)
        )

        screen_y = max(
            0.0,
            min(1.0, screen_y)
        )

        return screen_x, screen_y