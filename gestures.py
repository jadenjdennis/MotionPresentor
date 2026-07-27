import mediapipe as mp

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


    @staticmethod
    def getBoundingBox(hand_landmarks):
        xMin, yMin, xMax, yMax = 1.0, 1.0, 0.0, 0.0
        for lm in hand_landmarks.landmark:
            xMin, xMax = min(xMin, lm.x), max(xMax, lm.x)
            yMin, yMax = min(yMin, lm.y), max(yMax, lm.y)
        xMin, yMin = max(0, min(xMin, 1.0)), max(0, min(yMin, 1.0))
        xMax, yMax = max(0, min(xMax, 1.0)), max(0, min(yMax, 1.0))
        return xMin, yMin, xMax, yMax
