from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from werkzeug.exceptions import BadRequest

from app.core.generate.ids import id_generator
from app.core.settings import config
from app.db.configs.connection import db
from app.services.image import ImageService

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
        
        filename = id_generator() + '--' + secure_filename(file.filename)
        
        file.save(os.path.join(config.UPLOAD_FOLDER, filename))
        
        with db as session:
            try:
                service = ImageService(session)
                
                data = service.add(image_id=filename, filter_name='gray')
                
                return jsonify(data), 200
            except Exception as e:
                raise BadRequest(description=str(e))
    
    return jsonify(error="File type not allowed"), 400