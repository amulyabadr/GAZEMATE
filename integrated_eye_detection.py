import cv2
import mediapipe as mp


# MediaPipe setup

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils


# Eye landmark indices

LEFT_EYE = [
    362, 382, 381, 380,
    374, 373, 390, 249,
    263, 466, 388, 387,
    386, 385, 384, 398
]

RIGHT_EYE = [
    33, 7, 163, 144,
    145, 153, 154, 155,
    133, 173, 157, 158,
    159, 160, 161, 246
]


# Iris landmark indices

LEFT_IRIS = [474, 475, 476, 477]

RIGHT_IRIS = [469, 470, 471, 472]


def draw_eye_landmarks(frame, landmarks, eye_indices):

    height, width, _ = frame.shape

    points = []

    for index in eye_indices:

        landmark = landmarks.landmark[index]

        x = int(landmark.x * width)
        y = int(landmark.y * height)

        points.append((x, y))

        cv2.circle(
            frame,
            (x, y),
            3,
            (0, 255, 0),
            -1
        )

    return points


def draw_iris(frame, landmarks, iris_indices):

    height, width, _ = frame.shape

    points = []

    for index in iris_indices:

        landmark = landmarks.landmark[index]

        x = int(landmark.x * width)
        y = int(landmark.y * height)

        points.append((x, y))

        cv2.circle(
            frame,
            (x, y),
            4,
            (0, 0, 255),
            -1
        )

    return points


def draw_eye_box(frame, points, label):

    if not points:
        return

    x_values = [point[0] for point in points]
    y_values = [point[1] for point in points]

    x1 = min(x_values) - 8
    y1 = min(y_values) - 8

    x2 = max(x_values) + 8
    y2 = max(y_values) + 8

    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (255, 0, 0),
        2
    )

    cv2.putText(
        frame,
        label,
        (x1, y1 - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (255, 0, 0),
        2
    )


def detect_face_and_eyes(frame, face_mesh):

    # Convert BGR to RGB

    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    # Process frame

    results = face_mesh.process(rgb_frame)

    face_detected = False
    left_eye_detected = False
    right_eye_detected = False
    iris_detected = False

    if results.multi_face_landmarks:

        face_detected = True

        face_landmarks = (
            results.multi_face_landmarks[0]
        )

        # Draw face mesh

        mp_drawing.draw_landmarks(
            image=frame,
            landmark_list=face_landmarks,
            connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None,
            connection_drawing_spec=mp_drawing.DrawingSpec(
                color=(180, 180, 180),
                thickness=1,
                circle_radius=1
            )
        )

        # Left eye

        left_eye_points = draw_eye_landmarks(
            frame,
            face_landmarks,
            LEFT_EYE
        )

        if left_eye_points:
            left_eye_detected = True

        draw_eye_box(
            frame,
            left_eye_points,
            "LEFT EYE"
        )

        # Right eye

        right_eye_points = draw_eye_landmarks(
            frame,
            face_landmarks,
            RIGHT_EYE
        )

        if right_eye_points:
            right_eye_detected = True

        draw_eye_box(
            frame,
            right_eye_points,
            "RIGHT EYE"
        )

        # Left iris

        left_iris_points = draw_iris(
            frame,
            face_landmarks,
            LEFT_IRIS
        )

        # Right iris

        right_iris_points = draw_iris(
            frame,
            face_landmarks,
            RIGHT_IRIS
        )

        if left_iris_points and right_iris_points:
            iris_detected = True

    return (
        frame,
        face_detected,
        left_eye_detected,
        right_eye_detected,
        iris_detected,
        results.multi_face_landmarks
        if results.multi_face_landmarks
        else None
    )


if __name__ == "__main__":

    camera = cv2.VideoCapture(0)

    if not camera.isOpened():

        print("ERROR: Could not open webcam.")

    else:

        print("GazeMate - Integrated Face & Eye Detection")
        print("Press Q to exit.")

        with mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        ) as face_mesh:

            while True:

                success, frame = camera.read()

                if not success:
                    break

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

                cv2.imshow(
                    "GazeMate - Integrated Face & Eye Detection",
                    frame
                )

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

        camera.release()
        cv2.destroyAllWindows()