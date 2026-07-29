import mediapipe as mp
import numpy as np

class GestureDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode = False,
            max_num_hands = 1,
            min_detection_confidence = 0.5,
            min_tracking_confidence = 0.7
        )
    
    def processFrame(self, frame):
        self.result = self.hands.process(frame)

        #Even though the program doesn't need this, it's good practice to return the result anyways incase we want to use it.
        #Also it's another safety block, so if result doesn't exist, it won't check result.multi_hand_landmarks
        return self.result

    #This function is gonna be used to find the relation between two landmarks. Goal to see if result = (-) or (+)
    #I'll be using the distance formula for this function
    def getLandmarkRelation(self, hand_landmarks, lm1,lm2, image_width, image_height):
        lm1X, lm1Y = hand_landmarks.landmark[lm1].x, hand_landmarks.landmark[lm1].y
        lm2X, lm2Y = hand_landmarks.landmark[lm2].x, hand_landmarks.landmark[lm2].y

        lm1XCoord, lm1YCoord = int(lm1X * image_width), int(lm1Y * image_height)
        lm2XCoord, lm2YCoord = int(lm2X * image_width), int(lm2Y * image_height)

        #Now we do the calculation and return result: d = sqrt((x2 - x1)^2 + (y2 - y1)^2)
        result = lm2XCoord - lm1XCoord

        #Here I can tell if the result is (+) or (-), and return a boolean value which I can utilize in main.py 
        returnVal = False 
        if(result > 0):
            returnVal = True

        return returnVal


    @staticmethod
    def getBoundingBox(hand_landmarks):
        xMin, yMin, xMax, yMax = 1.0, 1.0, 0.0, 0.0
        for lm in hand_landmarks.landmark:
            xMin, xMax = min(xMin, lm.x), max(xMax, lm.x)
            yMin, yMax = min(yMin, lm.y), max(yMax, lm.y)
        xMin, yMin = max(0, min(xMin, 1.0)), max(0, min(yMin, 1.0))
        xMax, yMax = max(0, min(xMax, 1.0)), max(0, min(yMax, 1.0))
        return xMin, yMin, xMax, yMax
