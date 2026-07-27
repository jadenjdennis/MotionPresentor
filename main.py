import cv2
from camera import Camera
from gestures import GestureDetector
import overlay

cam = Camera(0)
detector = GestureDetector()

while True:
    ok, frame = cam.readFrame()
    if not ok:
        print("Error: Couldn't receive frame... Exiting program...")
        break

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

    cv2.imshow("Camera Feed", cv2.flip(frame, 1))
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.releaseFrame()
cv2.destroyAllWindows()
