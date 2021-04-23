from flask import Flask, render_template, Response,session,request, redirect, url_for
import cv2
import sys
import os
sys.path.append('../models/')
sys.path.append('../')
import models
import urllib.request
from app import app, UPLOAD_FOLDER
from werkzeug.utils import secure_filename
from flask import Blueprint
image_blueprint = Blueprint('upload', __name__,)



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


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@image_blueprint.route('/')
def upload_form():
	return render_template('upload.html')

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



@image_blueprint.route('/image/<filename>/<filter_index>',endpoint='image')
def return_img(filename, filter_index):
	filter_index = int(filter_index)


	return Response(get_image(filename, filter_index), mimetype='multipart/x-mixed-replace; boundary=frame')

def get_image(filename, filter_index):
    frame = cv2.imread(UPLOAD_FOLDER+filename)
    frame = filters(frame, filter_index)
    ret, buffer = cv2.imencode('.jpg', frame)
    frame = buffer.tobytes()
    return (b'--frame\r\n' + b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result