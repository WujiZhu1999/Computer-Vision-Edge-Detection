from flask import render_template, Response
import cv2
import sys
sys.path.append('../models/')
import models
from flask import Blueprint
camera_blueprint = Blueprint('camera', __name__,)
real_camera = cv2.VideoCapture(0)  # use 0 for web camera


#--------------------helper function starts here-----------------------#

#transfer image with specified index as filter
#0 no filter
#1 sobel gray
#2 sobel rgb
#3 canny
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


#generate frames which used for real time image
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


#--------------------route start here---------------------------#

#for processing real time image from web cam
@camera_blueprint.route('/video_feed/<index>')
def video_feed(index):
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(index), mimetype='multipart/x-mixed-replace; boundary=frame')

#for render real time web cam page
@camera_blueprint.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')