from flask import Blueprint, jsonify, request
from ..controllers import usuario_controller, producto_controller

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    resultado = usuario_controller.login_usuario(data)
    return jsonify(resultado), 200

@api.route('/registrar', methods=['POST'])
def register_user():
    data = request.get_json()
    resultado, status_code = usuario_controller.registrar_usuario(data)
    return jsonify(resultado), status_code

@api.route('/productos', methods=['GET'])
def get_all_productos():
    productos, status_code = producto_controller.get_all_productos()
    return jsonify(productos), status_code

@api.route('/productos/<int:producto_id>', methods=['GET'])
def get_producto(producto_id):
    producto, status_code = producto_controller.get_producto_by_id(producto_id)
    return jsonify(producto), status_code

@api.route('/productos', methods=['POST'])
def create_producto():
    data = request.get_json()
    producto, status_code = producto_controller.create_producto(data)
    return jsonify(producto), status_code

@api.route('/productos/<int:producto_id>', methods=['PUT'])
def update_producto(producto_id):
    data = request.get_json()
    producto, status_code = producto_controller.update_producto(producto_id, data)
    return jsonify(producto), status_code
