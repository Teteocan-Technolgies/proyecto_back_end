from flask import Blueprint, jsonify, request
from ..models.models import Usuario
from ..controllers import usuario_controller

api = Blueprint('api', __name__)

@api.route('/login', methods=['GET'])
def login_user():
    data = request.get_json()
    resultado = usuario_controller.login_usuario(data)
    return jsonify(resultado), 201

@api.route('/registrar', methods=['POST'])
def register_user():
    data = request.get_json()
    resultado = usuario_controller.registrar_usuario(data)
    return jsonify(resultado), 201
