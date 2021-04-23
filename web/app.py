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



##---------------------------------------------##

##_____________________________________________##
# this part responsible for image upload and processing

from image import image_blueprint
app.register_blueprint(image_blueprint, url_prefix='/upload')
from camera import camera_blueprint
app.register_blueprint(camera_blueprint, url_prefix='/camera')






##---------------------------------------------##

##_____________________________________________##
# this part responsible for real time processing
## for real time filters


if __name__ == '__main__':
    app.run(debug=True)