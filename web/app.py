from flask import Flask, render_template
import sys
sys.path.append('./models/')
UPLOAD_FOLDER = './uploads/'

#--------------start flask app-------------------#
app = Flask(__name__, template_folder = './templates', static_folder = './static')
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


##register route
from image import image_blueprint
app.register_blueprint(image_blueprint, url_prefix='/upload')

from camera import camera_blueprint
app.register_blueprint(camera_blueprint, url_prefix='/camera')


#main page
@app.route('/')
def index():
	return render_template('index.html')
#run the app
if __name__ == '__main__':
    app.run(debug=True)