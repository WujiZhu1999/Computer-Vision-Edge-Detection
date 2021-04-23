from flask import Flask, render_template, Response,session,request, redirect, url_for
import cv2
import sys
import os
sys.path.append('../models/')
sys.path.append('./models/')
import models
import urllib.request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './uploads/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

camera = cv2.VideoCapture(0)  # use 0 for web camera

##---------------------------------------------##

##_____________________________________________##
# this part responsible for image upload and processing

from image import image_blueprint
app.register_blueprint(image_blueprint, url_prefix='/upload')







##---------------------------------------------##

##_____________________________________________##
# this part responsible for real time processing
## for real time filters
def filters(img, filter_index):
	if filter_index == 0:
		return img
	elif filter_index == 1:
		return models.my_sobel(img)
	elif filter_index == 2:
		return models.my_sobel(img,gray_scale =False)
	elif filter_index == 3:
		return models.my_canny(img)
	else:
		return img

def gen_frames(filter_index):  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame

        frame = filters(frame, int(filter_index))
        #s()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed/<index>')
def video_feed(index):
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(index), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)