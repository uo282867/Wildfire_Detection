########### TODO ###########
'''
Test on JetsonNano
'''
############################
import cv2

class Camera:
    def __init__(self):
        pass

    def configure(self):
        pass
    
    def start(self):
        self.cam = cv2.VideoCapture(0)

    def isOpen(self):
        return self.cam.isOpened()
    
    def getFrame(self):
        ret, frame = self.cam.read()
        return frame