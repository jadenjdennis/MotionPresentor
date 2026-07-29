import cv2

#All this class does is initialize the camera and set it up for reading frames. It also has a function to read the current frame and return it.
class Camera:
    def __init__(self, camera_index = 0):
        self.cap = cv2.VideoCapture(camera_index)

        if not self.cap.isOpened():
            exit()

    #All this does is read the current fram from the camera and return it.
    #If not successful, then it prints and error message and exits the program.
    def readFrame(self):
        isSuccess, frame = self.cap.read()

        if not isSuccess:
            print("Error: Couldn't receive frame... Exiting program...")
            exit()
        
        return isSuccess, frame

    def releaseFrame(self):
        self.cap.release()
    
