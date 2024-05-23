from typing import Any
from mediapipe.python.solutions import objectron  # type: ignore
import mediapipe as mp  # type: ignore
import cv2
from cv2.typing import MatLike
from detectors import Detector
import numpy as np


class ObjectDetector3D(Detector):
    def __init__(self, model_name: str = "Shoe"):
        self.mp_drawing = mp.solutions.drawing_utils
        self.objectDetector = objectron.Objectron(
            model_name=model_name,
            min_tracking_confidence=0.5,
            min_detection_confidence=0.3,
        )

    def find(self, img: MatLike) -> Any:
        return self.objectDetector.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

    def draw(self, img: MatLike, res) -> MatLike:
        if res.detected_objects:
            for detected_object in res.detected_objects:
                if not detected_object.landmarks_2d:
                    return img
                if img.shape[2] != 3:
                    raise ValueError("Input image must contain three channel bgr data.")
                image_rows, image_cols, _ = img.shape
                idx_to_coordinates = {}
                for idx, landmark in enumerate(detected_object.landmarks_2d.landmark):
                    if (
                        landmark.HasField("visibility") and landmark.visibility < 0.5
                    ) or (landmark.HasField("presence") and landmark.presence < 0.5):
                        continue
                    landmark_px = self.mp_drawing._normalized_to_pixel_coordinates(
                        landmark.x, landmark.y, image_cols, image_rows
                    )
                    if landmark_px:
                        idx_to_coordinates[idx] = landmark_px
                if objectron.BOX_CONNECTIONS:
                    num_landmarks = len(detected_object.landmarks_2d.landmark)
                    # Draws the connections if the start and end landmarks are both visible.
                    for connection in objectron.BOX_CONNECTIONS:
                        start_idx = connection[0]
                        end_idx = connection[1]
                        if not (
                            0 <= start_idx < num_landmarks
                            and 0 <= end_idx < num_landmarks
                        ):
                            raise ValueError(
                                f"Landmark index is out of range. Invalid connection "
                                f"from landmark #{start_idx} to landmark #{end_idx}."
                            )
                        if (
                            start_idx in idx_to_coordinates
                            and end_idx in idx_to_coordinates
                        ):
                            cv2.line(
                                img,
                                idx_to_coordinates[start_idx],
                                idx_to_coordinates[end_idx],
                                (0, 255, 255),
                                2,
                            )
                    for idx, landmark_px in idx_to_coordinates.items():
                        cv2.circle(img, landmark_px, 2, (0, 255, 255), 2)
                        cv2.circle(img, landmark_px, 3, (0, 255, 255), 2)
                    image_rows, image_cols, _ = img.shape
                # Create axis points in camera coordinate frame.
                axis_world = np.float32([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])  # type: ignore
                axis_cam = (
                    np.matmul(detected_object.rotation, 0.1 * axis_world.T).T
                    + detected_object.translation
                )
                x = axis_cam[..., 0]
                y = axis_cam[..., 1]
                z = axis_cam[..., 2]
                # Project 3D points to NDC space.
                fx, fy = (1, 1)
                px, py = (0, 0)
                x_ndc = np.clip(-fx * x / (z + 1e-5) + px, -1.0, 1.0)
                y_ndc = np.clip(-fy * y / (z + 1e-5) + py, -1.0, 1.0)
                # Convert from NDC space to image space.
                x_im = np.int32((1 + x_ndc) * 0.5 * image_cols)
                y_im = np.int32((1 - y_ndc) * 0.5 * image_rows)
                # Draw xyz axis on the image.
                origin = (x_im[0], y_im[0])  # type:ignore
                z_axis = (x_im[3], y_im[3])  # type:ignore
                cv2.arrowedLine(img, origin, z_axis, (255, 0, 0), 2)
        return img


def main():
    detector = ObjectDetector3D()
    cap = cv2.VideoCapture(0)
    while True:
        (_, img) = cap.read()
        info = detector.find(img)
        cv2.imshow("Image", detector.draw(img, info))
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
