import cv2
from cvzone.FaceDetectionModule import FaceDetector
import gtts as gTTS

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

Detector = FaceDetector()

while True:
    (success, img) = cap.read()
    (img, bboxs) = Detector.findFaces(img, draw=True)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
