from ultralytics import YOLO
import cv2
import time
import os
import json
from camera.picam2 import Camera

from notify import send_notification


#####################################     READ CONFIG FILE   #################################################

with open('config.json', 'r') as f:
    config = json.load(f)

filterDict = {"predicts" : 0, "fails" : 0}

#####################################      CAMERA SET UP     #################################################

cam = Camera()
cam.configure()
cam.start()

#####################################  MODEL AND DIR SET UP  #################################################

# models_names = ['5_mu', '5_nu', '5_xu', '8_n', '8_s', '8_m', '8_l', '8_x', '9_c']
# m = models_names[3]

model = YOLO(config['model']['path'] + config['model']['name'])

if(config['debug']):
    savePath = config['output']['path']
    if not os.path.isdir(savePath): 
        os.makedirs(savePath)
    savePath+= '/'
    c = 1

#####################################       MAIN CODE       #################################################

# Check cam is working
if cam.isOpen() == False:
    print("Couldn't open the camera.")
else:
    print("Camera opened. Press 'q' to exit.")

# Capture frame by frame
while cam.isOpen():
    frame = cam.getFrame()

    # Check for fire or smoke
    results = model.predict(frame, conf=config['model']['conf'])

    # Save the image if something is detected
    info = results[0].verbose()
    if '(no detections)' not in info:
        if(config['debug']):    
            fn = savePath + f'img_{c}.jpg'
            results[0].save(filename=fn)
            print('Img saved in:', fn)
            time.sleep(1)
            c += 1
            c %= config['output']['img_limit'] # Max of images to avoid run out of memory

        filterDict['predicts'] += 1
        filterDict['fails'] = 0

        if filterDict['predicts'] >= config['model']['needed_predicts'] :
            _, img_encoded = cv2.imencode('.jpg', results[0].plot())
            img_bytes = img_encoded.tobytes()
            send_notification(info[:-2], img_bytes)
            time.sleep(config['server']['notification_delay'])
            filterDict['fails'] , filterDict['predicts'] = 0

    else:
        filterDict['fails'] += 1
        if filterDict['fails'] >= config['model']['reset_margin'] :
            filterDict['fails'] , filterDict['predicts'] = 0
        
    time.sleep(config['model']['delay'])    
    
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break    

