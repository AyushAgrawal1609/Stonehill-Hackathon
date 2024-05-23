import cv2
from ObjectDetector2D import ObjectDetector2D
from FaceDetector import FaceDetector
from ObjectDetector3D import ObjectDetector3D

detector = ObjectDetector2D()
detector = (ObjectDetector3D()) + detector + (FaceDetector())
cap = cv2.VideoCapture(0)
while True:
    (_, img) = cap.read()
    info = detector.find(img)
    cv2.imshow("Image", detector.draw(img, info))
    cv2.waitKey(1)
