from typing import Any, List, Tuple
from cv2.typing import MatLike
import mediapipe as mp
import cv2

from detectors import Detector


class FaceDetector(Detector):
    def __init__(self, minDetectionCon: float = 0.5) -> None:
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def find(self, img: MatLike, draw: bool = True) -> List:
        self.results = self.faceDetection.process(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        bboxs = []
        if self.results.detections:
            for id, detection in enumerate(self.results.detections):
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, ic = img.shape
                bbox = (
                    int(bboxC.xmin * iw),
                    int(bboxC.ymin * ih),
                    int(bboxC.width * iw),
                    int(bboxC.height * ih),
                )
                cx, cy = bbox[0] + (bbox[2] // 2), bbox[1] + (bbox[3] // 2)
                bboxInfo = {
                    "id": id,
                    "bbox": bbox,
                    "score": detection.score,
                    "center": (cx, cy),
                }
                bboxs.append(bboxInfo)

        return bboxs

    def draw(self, img: MatLike, information) -> MatLike:
        for info in information:
            img = cv2.rectangle(img, info["bbox"], (0, 255, 255), 2)

            cv2.putText(
                img,
                f'{int(info["score"][0] * 100)}%',
                (info["bbox"][0], info["bbox"][1] - 20),
                cv2.FONT_HERSHEY_DUPLEX,
                2,
                (255, 0, 0),
                2,
            )
        return img


def main():
    detector = FaceDetector()
    cap = cv2.VideoCapture(0)
    while True:
        (success, img) = cap.read()
        info = detector.find(img)
        cv2.imshow("Image", detector.draw(img, info))
        cv2.waitKey(1)


if __name__ == "__main__":
    main()
