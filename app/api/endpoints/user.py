from flask import (
    Blueprint, 
    jsonify, 
    request
)
from werkzeug.exceptions import BadRequest, InternalServerError

from app.db.configs.connection import db
from app.schemas.user import (
    UserRequest
)
from app.services.user import UserService

router = Blueprint('user', __name__, url_prefix='/user')

@router.route('/', methods=['POST'])
def create_user():
    """
    Cria um novo usuário no banco de dados. Todos os parâmetros devem ser enviados pelo body da requisição.
    ---
    parameters:
      - name: name
        in: body
        type: string
        required: true
      - name: phone
        in: body
        type: string
        required: true
      - name: email
        in: body
        type: string
        required: true
      - name: password
        in: body
        type: string
        required: true
    responses:
      200:
        description: User created successfully
      400:
        description: Invalid input
    """
    
    body = request.get_json()
    
    if not body:
        raise BadRequest(description="Invalid input")
    
    try:
        user_request = UserRequest(**body)
    except Exception as e:
        raise BadRequest(description=str(e))
    
    with db as session:
        try:
            service = UserService(session)
            response = service.add(user_request)
            return jsonify(response.to_dict()), 200
        except Exception as e:
            raise InternalServerError(description=str(e))

@router.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify(error=str(e)), 400

@router.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    return jsonify(error=str(e)), 500