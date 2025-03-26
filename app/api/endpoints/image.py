from flask import Blueprint, request, jsonify, send_from_directory
import os
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest

from app.core.constants.enums.user import ImageFilters
from app.core.generate.ids import id_generator
from app.core.settings import config
from app.db.configs.connection import db
from app.services.image import ImageService

router = Blueprint('image', __name__, url_prefix='/image')

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

@router.route('/<selected_filter>', methods=['POST'])
def upload_image(selected_filter: str):
    # Verifica se o arquivo está na requisição
    if selected_filter not in ImageFilters.values():
        return jsonify(error="Filter not found"), 400
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    
    file = request.files['file']
    
    # Verifica se o arquivo tem um nome válido
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    
    if file and allowed_file(file.filename):
        
        filename = id_generator() + '--' + secure_filename(file.filename)
        
        file.save(os.path.join(config.UPLOAD_FOLDER, filename))
        
        with db as session:
            try:
                service = ImageService(session)
                
                data = service.add(image_id=filename, filter_name=selected_filter)
                
                return jsonify(data), 200
            except Exception as e:
                raise BadRequest(description=str(e))
    
    return jsonify(error="File type not allowed"), 400

@router.route('/uploads/<filename>', methods=['GET'])
def get_uploaded_file(filename):
    return send_from_directory(config.UPLOAD_FOLDER, filename)

@router.route('/uploads/filtered/<filename>', methods=['GET'])
def get_uploaded_file_filtered(filename):
    return send_from_directory(config.UPLOAD_FOLDER_FILTERED, filename)