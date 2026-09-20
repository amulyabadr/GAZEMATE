import numpy as np


# ============================================================
# MediaPipe Iris Landmarks
# ============================================================

LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]


# ============================================================
# Eye Boundary Landmarks
# ============================================================

# Left eye
LEFT_EYE_LEFT = 362
LEFT_EYE_RIGHT = 263
LEFT_EYE_TOP = 386
LEFT_EYE_BOTTOM = 374

# Right eye
RIGHT_EYE_LEFT = 33
RIGHT_EYE_RIGHT = 133
RIGHT_EYE_TOP = 159
RIGHT_EYE_BOTTOM = 145


def get_iris_center(landmarks, iris_indices):

    x_values = []
    y_values = []

    for index in iris_indices:

        landmark = landmarks[index]

        x_values.append(landmark.x)
        y_values.append(landmark.y)

    if not x_values:
        return None

    center_x = np.mean(x_values)
    center_y = np.mean(y_values)

    return center_x, center_y


def get_eye_position(
    landmarks,
    iris_indices,
    eye_left,
    eye_right,
    eye_top,
    eye_bottom
):

    iris = get_iris_center(
        landmarks,
        iris_indices
    )

    if iris is None:
        return None

    iris_x, iris_y = iris

    # --------------------------------------------------------
    # Eye horizontal range
    # --------------------------------------------------------

    left_x = landmarks[eye_left].x
    right_x = landmarks[eye_right].x

    eye_width = abs(right_x - left_x)

    if eye_width < 0.001:
        return None

    min_x = min(left_x, right_x)

    ratio_x = (
        iris_x - min_x
    ) / eye_width

    # --------------------------------------------------------
    # Eye vertical range
    # --------------------------------------------------------

    top_y = landmarks[eye_top].y
    bottom_y = landmarks[eye_bottom].y

    eye_height = abs(bottom_y - top_y)

    if eye_height < 0.001:
        return None

    min_y = min(top_y, bottom_y)

    ratio_y = (
        iris_y - min_y
    ) / eye_height

    return ratio_x, ratio_y


def estimate_gaze(
    landmarks,
    frame_width,
    frame_height
):

    if landmarks is None:
        return None

    # ========================================================
    # Left eye
    # ========================================================

    left_position = get_eye_position(
        landmarks,
        LEFT_IRIS,
        LEFT_EYE_LEFT,
        LEFT_EYE_RIGHT,
        LEFT_EYE_TOP,
        LEFT_EYE_BOTTOM
    )

    # ========================================================
    # Right eye
    # ========================================================

    right_position = get_eye_position(
        landmarks,
        RIGHT_IRIS,
        RIGHT_EYE_LEFT,
        RIGHT_EYE_RIGHT,
        RIGHT_EYE_TOP,
        RIGHT_EYE_BOTTOM
    )

    if (
        left_position is None
        or right_position is None
    ):
        return None

    left_x, left_y = left_position
    right_x, right_y = right_position

    # ========================================================
    # Average both eyes
    # ========================================================

    gaze_x = (
        left_x + right_x
    ) / 2.0

    gaze_y = (
        left_y + right_y
    ) / 2.0

    # ========================================================
    # Keep values within normalized range
    # ========================================================

    gaze_x = max(
        0.0,
        min(1.0, gaze_x)
    )

    gaze_y = max(
        0.0,
        min(1.0, gaze_y)
    )

    return gaze_x, gaze_y


if __name__ == "__main__":

    print("GazeMate - Gaze Estimation")

    print(
        "Gaze is estimated using iris position "
        "relative to the eye boundaries."
    )