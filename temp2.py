# from mediapipe.python.solutions import objectron
# import mediapipe as mp
# import cv2

# cap = cv2.VideoCapture(0)
# ax = [0, 0, 0, 0, 0]
# ay = [0, 0, 0, 0, 0]
# az = [0, 0, 0, 0, 0]

# mp_drawing = mp.solutions.drawing_utils
# objectDetector = objectron.Objectron(
#     model_name="Chair", min_tracking_confidence=0.5, min_detection_confidence=0.3
# )
# a = True
# while a:
#     (success, img) = cap.read()
#     if success:
#         imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
#         bboxs = objectDetector.process(imgRGB)
#         if bboxs.detected_objects:
#             for detected_object in bboxs.detected_objects:
#                 mp_drawing.draw_landmarks(
#                     img, detected_object.landmarks_2d, objectron.BOX_CONNECTIONS
#                 )
#                 ax.append(detected_object.rotation[0][0])
#                 ax.pop(0)
#                 ay.append(detected_object.rotation[0][1])
#                 ay.pop(0)
#                 az.append(detected_object.rotation[0][2])
#                 az.pop(0)
#                 d = 0
#                 for i in ax:
#                     d += i
#                 print("x: " + str(d))
#                 d = 0
#                 for i in ay:
#                     d += i
#                 print("y: " + str(d))
#                 d = 0
#                 for i in az:
#                     d += i
#                 print("z: " + str(d))
#                 mp_drawing.draw_axis(
#                     img, detected_object.rotation, detected_object.translation
#                 )

#         cv2.imshow("Image", img)
#         cv2.waitKey(1)
import cv2
from ObjectDetector2D import ObjectDetector2D
from FaceDetector import FaceDetector

detector = ObjectDetector2D()
detector2 = FaceDetector()
detector = detector + detector2
cap = cv2.VideoCapture(0)
while True:
    (success, img) = cap.read()
    info = detector.find(img)
    cv2.imshow("Image", detector.draw(img, info))
    cv2.waitKey(1)
