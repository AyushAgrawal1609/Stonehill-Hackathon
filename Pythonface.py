import cv2
from cvzone.FaceDetectionModule import FaceDetector
from gtts import gTTS
import os

cap = cv2.VideoCapture(0)

cap.set(3, 640)
cap.set(4, 480)

people = 0


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
        Speaker = gTTS(NumberToName(people) + " people here", lang="en")
        Speaker.save("PeopleHere.mp3")
        os.system("start PeopleHere.mp3")

    cv2.imshow("Image", img)
    cv2.waitKey(1)
