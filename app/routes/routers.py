from flask import Blueprint, jsonify, request
from ..controllers import usuario_controller

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    resultado = usuario_controller.login_usuario(data)
    return jsonify(resultado), 200

@api.route('/registrar', methods=['POST'])
def register_user():
    resultado, status_code = usuario_controller.registrar_usuario(request.get_json())
    return jsonify(resultado), status_code
