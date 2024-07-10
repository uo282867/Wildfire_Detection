import requests
import cv2
import json
import numpy as np

class Camera:
    def __init__(self):
        pass
    
    def configure(self):
        with open('config.json', 'r') as f:
            self.config = json.load(f)
    
    def start(self):
        pass

    def isOpen(self):
        try:
            # print(self.config['httpcam']['health'])
            response = requests.get(self.config['httpcam']['health'])
            if response.status_code == 200 and response.json().get("status") == "running":
                return True
        except requests.ConnectionError:
            pass
        return False
    
    def getFrame(self):
        try:
            response = requests.get(self.config['httpcam']['img'])
            if response.status_code == 200:
                image_array = np.frombuffer(response.content, dtype=np.uint8)
                frame = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                if frame is not None:
                    return frame
                else:
                    raise Exception('Error while decoding the image')

        except requests.ConnectionError:
            pass
        raise Exception('Error, none response')

