from flask import Flask, render_template, Response,session,request, redirect, url_for
import cv2
import sys
import os
sys.path.append('../models/')
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

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload/')
def upload_form():
	return render_template('upload.html')

@app.route('/upload/', methods=['POST', 'GET'])
def upload_image():
	if 'files[]' not in request.files:
		flash('No file part')
		return redirect(request.url)
	files = request.files.getlist('files[]')
	file_names = []
	for file in files:
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file_names.append(filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		#else:
		#	flash('Allowed image types are -> png, jpg, jpeg, gif')
		#	return redirect(request.url)

	return render_template('upload.html', filenames=file_names)



@app.route('/upload/image/<filename>',endpoint='image')
def return_img(filename):
	return Response(get_image(filename), mimetype='multipart/x-mixed-replace; boundary=frame')

def get_image(filename):
    frame = cv2.imread(UPLOAD_FOLDER+filename)
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    return (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result










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