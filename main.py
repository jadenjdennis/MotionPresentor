import cv2
from camera import Camera
from gestures import GestureDetector
import overlay
import pyautogui as pg
import time

cam = Camera(0)
detector = GestureDetector()

cooldownDuration = 2.0
lastTriggerTime = 0.0

while True:
    ok, frame = cam.readFrame()
    if not ok:
        print("Error: Couldn't receive frame... Exiting program...")
        break

    currentTime = time.time()

    frame.flags.writeable = False
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = detector.processFrame(rgb_frame)

    

    #This is a safety block, so if result doesn't exist, it won't bother checking the other, which would throw an error
    if result and result.multi_hand_landmarks:
        hand_landmarks = result.multi_hand_landmarks[0]

        frame.flags.writeable = True
        overlay.drawHands(frame, hand_landmarks)
        box = detector.getBoundingBox(hand_landmarks)
        h, w = frame.shape[0], frame.shape[1]
        overlay.drawBoundingBox(frame, box, w, h)

        normLMs = detector.normalizeCoords(result.multi_hand_landmarks[0], w, h)

        #print(normLMs[5][0] - normLMs[0][0])

        #Here we are gonna use the getLandmarkRelation function to figure out if the user wants to go to the next or previous slide
        if(detector.getLandmarkRelation(normLMs[8], normLMs[0]) and (detector.getLandmarkRelation(normLMs[12], normLMs[0]))):
            if((not(detector.getLandmarkRelation(normLMs[16], normLMs[10]))) and (not(detector.getLandmarkRelation(normLMs[20], normLMs[10]))) and (detector.getLandmarkRelation(normLMs[11], normLMs[14]))):
                #Here's where we gotta use PyAutoGUI to click the arrow key forward
                if((currentTime - lastTriggerTime) >= cooldownDuration):
                    pg.press('right')
                    lastTriggerTime = currentTime
                    print("Gesture detected, right arrow key pressed.")
                #else:
                    #print("Gesture detected, but still in cooldown period. Please wait before triggering again.")
        elif((not(detector.getLandmarkRelation(normLMs[8], normLMs[0]))) and (not(detector.getLandmarkRelation(normLMs[12], normLMs[0])))):
            if(detector.getLandmarkRelation(normLMs[16], normLMs[10]) and (detector.getLandmarkRelation(normLMs[20], normLMs[10])) and (not(detector.getLandmarkRelation(normLMs[11], normLMs[14])))):
                #Here's where we gotta use PyAutoGUI to click the arrow key backwards
                if((currentTime - lastTriggerTime) >= cooldownDuration):
                    pg.press('left')
                    lastTriggerTime = currentTime
                    print("Gesture detected, left arrow key pressed.")
                #else:
                    #print("Gesture detected, but still in cooldown period. Please wait before triggering again.")



    cv2.imshow("Camera Feed", cv2.flip(frame, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.releaseFrame()
cv2.destroyAllWindows()
