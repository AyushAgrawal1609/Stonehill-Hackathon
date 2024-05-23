from typing import Any, Tuple
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from cv2.typing import MatLike
from detectors import Detector


class ObjectDetector2D(Detector):
    def __init__(self):

        # STEP 2: Create an ObjectDetector object.
        self.base_options = python.BaseOptions(
            model_asset_path="C:/Users/Admin/Documents/Stonehill Hackathon/ssd_mobilenet_v2.tflite"
        )
        self.options = vision.ObjectDetectorOptions(
            base_options=self.base_options, score_threshold=0.5
        )
        self.detector = vision.ObjectDetector.create_from_options(self.options)

    def find(self, img: MatLike) -> Any:
        return self.detector.detect(
            mp.Image(image_format=mp.ImageFormat.SRGB, data=img)
        )

    def draw(self, image, detection_result) -> np.ndarray:
        for detection in detection_result.detections:

            bbox = detection.bounding_box
            start_point = bbox.origin_x, bbox.origin_y
            end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
            cv2.rectangle(image, start_point, end_point, (0, 255, 255), 2)

            # Draw label and score
            category = detection.categories[0]
            category_name = category.category_name
            probability = round(category.score, 2)
            result_text = category_name + " (" + str(probability) + ")"
            text_location = (bbox.origin_x, bbox.origin_y - 20)
            cv2.putText(
                image,
                result_text,
                text_location,
                cv2.FONT_HERSHEY_DUPLEX,
                2,
                (255, 0, 0),
                2,
            )

        return image


def main():
    detector = ObjectDetector2D()
    cap = cv2.VideoCapture(0)
    while True:
        (success, img) = cap.read()
        info = detector.find(img)
        cv2.imshow("Image", detector.draw(img, info))
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
