import os
from flask import Flask, render_template, jsonify, request, Blueprint, send_from_directory, current_app
from libs.functions import allowed_file
from werkzeug.utils import secure_filename
ALLOWED_EXTENSIONS = {'jpg','png','jpeg'}

route_pictures = Blueprint('route_pictures', __name__)
@route_pictures.route('/upload', methods=['POST'])
@route_pictures.route('/upload/<filename>', methods=['GET, DELETE'])
def upload_file(filename=None):
    if request.method == 'GET':
        return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error":"not files present"}), 422

        file = request.files['file']
        if file.filename == '':
            return jsonify({"msg":"Please select a file"}), 422
        if file and allowed_file(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            return jsonify({"msg":"file uploaded"}), 200
        else:
            return jsonify({"msg":"file not allowed"}), 400 
    
    if request.method == 'DELETE':
        os.remove(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"msg":"file uploaded"}), 200