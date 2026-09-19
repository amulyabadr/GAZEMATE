import numpy as np


LEFT_IRIS = [
    474, 475, 476, 477
]

RIGHT_IRIS = [
    469, 470, 471, 472
]


LEFT_EYE_LEFT = 362
LEFT_EYE_RIGHT = 263

RIGHT_EYE_LEFT = 33
RIGHT_EYE_RIGHT = 133


def get_iris_center(
    landmarks,
    iris_indices
):

    x_values = []
    y_values = []

    for index in iris_indices:

        landmark = landmarks[index]

        x_values.append(
            landmark.x
        )

        y_values.append(
            landmark.y
        )

    if not x_values:

        return None

    center_x = np.mean(
        x_values
    )

    center_y = np.mean(
        y_values
    )

    return (
        center_x,
        center_y
    )


def get_eye_ratio(
    landmarks,
    iris_indices,
    eye_left,
    eye_right
):

    iris = get_iris_center(
        landmarks,
        iris_indices
    )

    if iris is None:
        return None

    iris_x = iris[0]

    left_x = landmarks[
        eye_left
    ].x

    right_x = landmarks[
        eye_right
    ].x

    eye_width = abs(
        right_x - left_x
    )

    if eye_width == 0:

        return None

    ratio_x = (
        iris_x
        - min(left_x, right_x)
    ) / eye_width

    return ratio_x


def estimate_gaze(
    landmarks,
    frame_width,
    frame_height
):

    if landmarks is None:

        return None

    left_ratio = get_eye_ratio(
        landmarks,
        LEFT_IRIS,
        LEFT_EYE_LEFT,
        LEFT_EYE_RIGHT
    )

    right_ratio = get_eye_ratio(
        landmarks,
        RIGHT_IRIS,
        RIGHT_EYE_LEFT,
        RIGHT_EYE_RIGHT
    )

    if (
        left_ratio is None
        or right_ratio is None
    ):

        return None

    # Average both eyes
    gaze_x = (
        left_ratio
        + right_ratio
    ) / 2

    left_iris = get_iris_center(
        landmarks,
        LEFT_IRIS
    )

    right_iris = get_iris_center(
        landmarks,
        RIGHT_IRIS
    )

    if (
        left_iris is None
        or right_iris is None
    ):

        return None

    gaze_y = (
        left_iris[1]
        + right_iris[1]
    ) / 2

    # Basic/coarse gaze estimation
    # Reduce precision deliberately for demonstration.
    gaze_x = round(
        gaze_x,
        1
    )

    gaze_y = round(
        gaze_y,
        1
    )

    gaze_x = max(
        0.0,
        min(1.0, gaze_x)
    )

    gaze_y = max(
        0.0,
        min(1.0, gaze_y)
    )

    return (
        gaze_x,
        gaze_y
    )


if __name__ == "__main__":

    print(
        "GazeMate - Basic Gaze Estimation"
    )

    print(
        "Gaze is estimated from iris position."
    )

    print(
        "The demonstration uses coarse coordinates."
    )