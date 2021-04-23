from flask import Flask
import sys
sys.path.append('./models/')
UPLOAD_FOLDER = './uploads/'

#--------------start flask app-------------------#
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


##register route
from image import image_blueprint
app.register_blueprint(image_blueprint, url_prefix='/upload')

from camera import camera_blueprint
app.register_blueprint(camera_blueprint, url_prefix='/camera')

#run the app
if __name__ == '__main__':
    app.run(debug=True)