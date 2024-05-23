import cv2
from gtts import gTTS
from cv2.typing import MatLike
import os
import mediapipe as mp

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

people = 0


class FaceDetector:

    def __init__(self, minDetectionCon: float = 0.5):
        self.minDetectionCon = minDetectionCon
        self.mpFaceDetection = mp.solutions.face_detection
        self.mpDraw = mp.solutions.drawing_utils
        self.faceDetection = self.mpFaceDetection.FaceDetection(self.minDetectionCon)

    def findFaces(self, img: MatLike, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.faceDetection.process(imgRGB)
        print(self.results)
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
                if draw:
                    img = cv2.rectangle(img, bbox, (255, 0, 255), 2)

                    cv2.putText(
                        img,
                        f"{int(detection.score[0] * 100)}%",
                        (bbox[0], bbox[1] - 20),
                        cv2.FONT_HERSHEY_PLAIN,
                        2,
                        (255, 0, 255),
                        2,
                    )
        return img, bboxs


def NumberToName(n):
    if n == 0:
        return "zero"
    elif n == 1:
        return "one"
    elif n == 2:
        return "two"
    elif n == 3:
        return "three"
    elif n == 4:
        return "four"
    elif n == 5:
        return "five"
    else:
        return "many"


Detector = FaceDetector()

while True:
    (success, img) = cap.read()
    (img, bboxs) = Detector.findFaces(img, draw=True)
    if len(bboxs) != people:
        people = len(bboxs)
        print(people)
        s = "people"
        if people == 1:
            s = "person"
        Speaker = gTTS(NumberToName(people) + " " + s + " here", lang="en")
        Speaker.save("PeopleHere.mp3")
        os.system("start PeopleHere.mp3")

    cv2.imshow("Image", img)
    cv2.waitKey(1)
