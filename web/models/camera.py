from flask import Flask, render_template, Response,session,request, redirect, url_for
import cv2
import sys
import os
sys.path.append('../models/')
import models
from app import app
from flask import Blueprint
camera_blueprint = Blueprint('camera', __name__,)

real_camera = cv2.VideoCapture(0)  # use 0 for web camera

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
        success, frame = real_camera.read()  # read the camera frame

        frame = filters(frame, int(filter_index))
        #s()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@camera_blueprint.route('/video_feed/<index>')
def video_feed(index):
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(index), mimetype='multipart/x-mixed-replace; boundary=frame')

@camera_blueprint.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')