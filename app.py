from flask import Flask, render_template, request, jsonify, send_file
import os
import cv2
from io import BytesIO
from PIL import Image
import numpy as np

from sklearn.datasets import load_files
from app_model import object_detection
from app_model import yolo_preds_for_real_time

from logger import logger



# webserver gateway interface
# we create an instace of thr flask class, which shall handle requests, routing, etc.
# __name__ argument is a special Python variable that represents the name of the current module.
app = Flask(__name__)

BASE_PATH = os.getcwd()
UPLOAD_PATH = os.path.join(BASE_PATH,'static/upload/')
DEFAULT_UPLOAD_PATH = os.path.join(BASE_PATH,'static/Verification/')
PREDICTIONS_PATH = os.path.join(BASE_PATH,'static/predict/')


# This is a route configured to respond to both GET and POST requests
# Used to define a route for the specified URL path
# Index function is executed whenever a request is sent to the specified URL path
# The logger object is imported from logger.py and it writes "Page Visited" in the file app.log
# The command render_tempelate index.html renders that html file which is present in the
# tempelate folder

@app.route('/',methods=['POST','GET'])
def index():
    logger.info('Page Visited')
    return render_template('index.html')

# This route is accessible through only the URL path '/process_uploaded_image' 
# It also only respons to POST requests



@app.route('/process_uploaded_image', methods=['POST'])
def process_uploaded_image():
    # get uploaded file
    
    logger.info('New image uploaded for detection')
    
    # This retrieves the image from the POST request
    image = request.files['image']
    
    # This particular filename is the actual name of the uploaded image
    filename = image.filename

    # This constructs the actual path where the image will be saved.
    # It concatenates th UPLOAD PATH the filename
    path_save = os.path.join(UPLOAD_PATH,filename)
    image.save(path_save)


    # The text is being predicted by using the object_detection fucntion present in 
    # the app_model.py file
    text = object_detection(path_save, filename)
    print(text)
    
    # This result is being returned to the frontend in the Json format
    return jsonify({
        'filename': filename,
        'text': text
    })

@app.route('/process_image', methods=['POST'])
def process_image():
    logger.info('Requested detection for an existing image')
    
    # request.form is used to handle the form data
    filename = request.form['file_name']

    path_save = os.path.join(DEFAULT_UPLOAD_PATH,filename)

    text = object_detection(path_save, filename)
    print(text)

    # Return the result to the front-end
    return jsonify(text=text)

# __name__ equals main means that this file should be run as the main file and not imported as a module
# if this file is being run as the main file in that case the app.run command runs
# the debug true means that 1.the server automatically reloads the app whenever there is a change
# in the code and 2.the error messages are elaborative
# 0.0.0.0 tells that the server should listen to all network interfaces.
# It means the Flask application will be accessible from any IP address, 
# both from the local machine and from external sources.
if __name__ =="__main__":
    app.run(host ='0.0.0.0', debug=True)