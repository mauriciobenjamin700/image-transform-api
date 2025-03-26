from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename

from app.core.settings import config

router = Blueprint('image', __name__, url_prefix='/image')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@router.route('/', methods=['POST'])
def upload_image():
    # Verifica se o arquivo está na requisição
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    
    file = request.files['file']
    
    # Verifica se o arquivo tem um nome válido
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(config.UPLOAD_FOLDER, filename))
        return jsonify(message="File uploaded successfully", filename=filename), 200
    
    return jsonify(error="File type not allowed"), 400