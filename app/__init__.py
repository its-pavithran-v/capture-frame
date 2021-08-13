import flask
import jinja2
import cv2
import os
import numpy as np
from flask import render_template, request, jsonify
from werkzeug import secure_filename
 
app = flask.Flask(__name__)
 
 
@app.route('/')
def upload_form():
    return render_template('capture_frame.html')
     
@app.route('/upload', methods=['POST'])
def upload_file():

    if 'files[]' not in request.files:
        resp = jsonify({'message' : 'No file part in the request'})
        resp.status_code = 400
        return resp
     
    files = request.files.getlist('files[]')
     
    errors = {}
    success = False

    path = os.path.join(os.getcwd(), 'app/static/')
    os.makedirs(os.path.join(path, 'vid_dir'), exist_ok=True)
    os.makedirs(os.path.join(path, 'frame_dir'), exist_ok=True)
     
    for file in files:
        if file:
            filepath = os.path.join(path, 'vid_dir', secure_filename(file.filename))
            file.save(filepath)
            vidcap = cv2.VideoCapture(filepath)
            frame_count = vidcap.get(cv2.CAP_PROP_FRAME_COUNT)
            frame = frame_count/2
            vidcap.set(cv2.CAP_PROP_POS_FRAMES, frame)
            success,image = vidcap.read()
            frame_of_video = file.filename + '.jpg'
            frame_dir_path = os.path.join(path, 'frame_dir')
            cv2.imwrite(os.path.join(frame_dir_path , frame_of_video), image) 
            img_src = "/static/frame_dir/" +  frame_of_video
            resp = jsonify(img_src)
            success = True
            print(resp)
            return resp
        else:
            errors[file.filename] = 'File type is not allowed'
            return resp
 
if __name__ == '__main__':
    app.run(debug=True)