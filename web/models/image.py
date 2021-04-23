from flask import render_template, Response,request, redirect
import cv2
import sys
import os
sys.path.append('../')
import models
import urllib.request
from app import app, UPLOAD_FOLDER
from werkzeug.utils import secure_filename
from flask import Blueprint
image_blueprint = Blueprint('upload', __name__,)

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

#for checking allowed file format: png,jpg,jpeg,gif
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#process the image with filter specified by the index
def get_image(filename, filter_index):
    frame = cv2.imread(UPLOAD_FOLDER+filename)
    frame = filters(frame, filter_index)
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    return (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

#--------------------route start here---------------------------#
#for render image processing
@image_blueprint.route('/')
def upload_form():
	return render_template('upload.html')

#for image upload and processing
@image_blueprint.route('/', methods=['POST', 'GET'])
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


#for displaying image with specified format
@image_blueprint.route('/image/<filename>/<filter_index>',endpoint='image')
def return_img(filename, filter_index):
	filter_index = int(filter_index)


	return Response(get_image(filename, filter_index), mimetype='multipart/x-mixed-replace; boundary=frame')

