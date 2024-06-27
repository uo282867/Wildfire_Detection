import requests
from PIL import Image
import io
import json

with open('config.json', 'r') as f:
    configuracion = json.load(f)

def send_notification(message, img_url):
    # Open and read the image
    with open(img_url, 'rb') as img_file:
        img_data = img_file.read()

    # Notification payload
    payload = {
        'title': 'WARNING: WildFire Detection',
        'message': message, 
        'key' : configuracion['server']['key']
    }
    

    # Send the image
    files = {
        'img': (img_url, img_data, 'image/png')
    }
    print(configuracion['server']['url'])

    # POST request
    response = requests.post(configuracion['server']['url'], data=payload, files=files)


    # Check status
    if response.status_code == 200:
        print('OK')
    else:
        print(f'ERROR: {response.status_code}')
