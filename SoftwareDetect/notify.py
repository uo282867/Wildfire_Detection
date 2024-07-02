import requests
from PIL import Image
import io
import json

with open('config.json', 'r') as f:
    config = json.load(f)

def send_notification(message, img):
    # Notification payload
    payload = {
        'title': 'WARNING: WildFire Detection',
        'message': message, 
        'key' : config['server']['key']
    }
    

    # Send the image
    files = {
        'img': ('predict.jpg', img, 'image/jpeg')
    }
    print(config['server']['url'])

    # POST request
    response = requests.post(config['server']['url'], data=payload, files=files)


    # Check status
    if response.status_code == 200:
        print('OK')
    else:
        print(f'ERROR: {response.status_code}')
