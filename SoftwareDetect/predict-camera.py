from ultralytics import YOLO
import cv2
import time
import os
import json
from camera.picam2 import Camera


from notify import send_notification

#####################################     READ CONFIG FILE   #################################################

with open('config.json', 'r') as f:
    configuracion = json.load(f)


#####################################      CAMERA SET UP     #################################################

cam = Camera()
cam.configure()
cam.start()

#####################################  MODEL AND DIR SET UP  #################################################

# models_names = ['5_mu', '5_nu', '5_xu', '8_n', '8_s', '8_m', '8_l', '8_x', '9_c']
# m = models_names[3]

model = YOLO(configuracion['model']['path'] + configuracion['model']['name'])

savePath = configuracion['output']['path']
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
    results = model.predict(frame)

    # Save the image if something is detected
    info = results[0].verbose()
    if '(no detections)' not in info:
        fn = savePath + f'img_{c}.jpg'
        results[0].save(filename=fn)

        print('Img saved in:', fn)
        time.sleep(1)
        
        send_notification(info[:-2], fn)
        time.sleep(configuracion['server']['notification_delay'])
        
        c += 1
        c %= configuracion['output']['img_limit'] # Max of images to avoid run out of memory
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break    

