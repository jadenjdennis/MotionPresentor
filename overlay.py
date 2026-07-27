import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils

def drawHands(frame, hand_landmarks):
    mp_drawing.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

def drawBoundingBox(frame, box, image_width, image_height):
    xMin, yMin, xMax, yMax = box
    xMinPix, yMinPix = int(xMin * image_width), int(yMin * image_height)
    xMaxPix, yMaxPix = int(xMax * image_width), int(yMax * image_height)
    cv2.rectangle(frame, (xMinPix, yMinPix), (xMaxPix, yMaxPix), (0, 255, 0), 5)
