import cv2

class Camera:
    def __init__(self, camera_index = 0):
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            exit()

    def readFrame(self):
        isSuccess, frame = self.cap.read()

        if not isSuccess:
            print("Error: Couldn't receive frame... Exiting program...")
            exit()
        
        return isSuccess, frame

    def releaseFrame(self):
        self.cap.release()
    
