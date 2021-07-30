import flask
import jinja2
import cv2
import os
import numpy as np
from flask import render_template, request, make_response, jsonify
from werkzeug import secure_filename

app = flask.Flask(__name__)


@app.route("/",methods=["GET", "POST"])
def capture_frame():
    if request.method == "GET":
        return render_template("capture_frame.html")

    if request.method == "POST":
        os.makedirs(os.path.join(os.getcwd(), 'vid_dir'), exist_ok=True)
        os.makedirs(os.path.join(os.getcwd(), 'frame_dir'), exist_ok=True)
        path = os.path.join(os.getcwd(), 'frame_dir')
        file = request.files['file']
        filepath = os.path.join(os.getcwd(), 'vid_dir', secure_filename(file.filename))
        file.save(filepath)
        vidcap = cv2.VideoCapture(filepath)
        frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
        frame = frame_count/2
        vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
        success,image = vidcap.read()
        frame_of_video = file.filename + '.jpg'
        cv2.imwrite(os.path.join(path , frame_of_video), image) 
        #ret, jpeg = cv2.imencode('.jpg', image)
        #response = make_response(jpeg.tobytes())
        #response.headers['Content-Type'] = 'image/png'
        return render_template("capture_frame.html") 


    
    