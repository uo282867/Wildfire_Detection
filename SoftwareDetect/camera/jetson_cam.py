import cv2
from flask import Flask, Response, jsonify

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=120,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "running"}), 200

@app.route('/img', methods=['GET'])
def get_img():
    _, frame = CAMERA.read()
    _, img = cv2.imencode('.jpg', frame)
    return Response(img.tobytes(), mimetype='image/jpeg', status=200)



if __name__ == '__main__':
    CAMERA = cv2.VideoCapture(gstreamer_pipeline(flip_method=0), cv2.CAP_GSTREAMER)
    if CAMERA.isOpened():
        print("Camera open")        
    else:
        print("Unable to open camera")
    
    app.run(port=5005)