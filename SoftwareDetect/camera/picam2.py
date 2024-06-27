from picamera2 import Picamera2

class Camera:
    def __init__(self):
        self.cam = Picamera2()

    def configure(self):
        self.cam.preview_configuration.main.size = (1280, 720)
        self.cam.preview_configuration.main.format = "RGB888"
        self.cam.preview_configuration.align()
        self.cam.configure("preview")

    def start(self):
        self.cam.start()

    def isOpen(self):
        return self.is_open
    
    def getFrame(self):
        return self.cam.capture_array()