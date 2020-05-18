from flask import Blueprint, jsonify, request, send_from_directory
from libs.functions import allowed_files
ALLOWED_EXTENSIONS = {'jpg','png','jpeg'}

images = Blueprint('images', __name__)
@images.route('/upload', methods=['POST'])
@images.route('/upload/<filename>', methods=['GET'])
def upload(filename=None):
    if request.method == 'GET':
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify({"error":"not files present"}), 422

        file = request.files['file']
        if file.filename == '':
            return jsonify({"msg":"Please select a file"}), 422
        if file and allowed_files(file.filename, ALLOWED_EXTENSIONS):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({"msg":"file uploaded"}), 200
        else:
            return jsonify({"msg":"file not allowed"}), 400  