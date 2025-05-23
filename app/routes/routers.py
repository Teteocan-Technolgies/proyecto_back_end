from flask import Blueprint, jsonify, request
from ..controllers import usuario_controller, producto_controller, venta_controller, chat_bot_controller, venta_detalle_controller

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

@api.route('/usuarios', methods=['GET'])
def get_all_data():
    usuarios, status_code = usuario_controller.get_all_users()
    return jsonify(usuarios), status_code

@api.route('/user/data/<int:usuario_id>', methods=['POST'])
def get_data_usuario(usuario_id):
    usuario, status_code = usuario_controller.get_data_usuario(usuario_id)
    return jsonify(usuario), status_code

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

@api.route('/productos/<int:producto_id>', methods=['DELETE'])
def delete_producto(producto_id):
    producto, status_code = producto_controller.delete_producto(producto_id)
    return jsonify(producto), status_code

@api.route('/ventas', methods=['GET'])
def get_all_ventas():
    ventas, status_code = venta_controller.get_all_ventas()
    return jsonify(ventas), status_code


@api.route('/ventas/<int:venta_id>', methods=['GET'])
def get_venta(venta_id):
    data, status_code = venta_controller.get_venta_by_id(venta_id)  # Ahora funcionará
    return jsonify(data), status_code

@api.route('/ventas/usuario/<int:usuario_id>', methods=['GET'])
def get_venta_by_usuario(usuario_id):
    ventas, status_code = venta_controller.get_ventas_by_cliente_id(usuario_id)
    return jsonify(ventas), status_code

@api.route('/ventas', methods=['POST'])
def create_venta():
    data = request.get_json()
    venta, status_code = venta_controller.create_venta(data)
    return jsonify(venta), status_code

@api.route('/ventas/<int:venta_id>', methods=['PUT'])
def update_venta(venta_id):
    data = request.get_json()
    venta, status_code = venta_controller.update_venta(venta_id, data)
    return jsonify(venta), status_code

@api.route('/ventas/<int:venta_id>', methods=['DELETE'])
def delete_venta(venta_id):
    venta, status_code = venta_controller.delete_venta(venta_id)
    return jsonify(venta), status_code

@api.route('/ventas/data', methods=['GET'])
def get_all_stadistics():
    ventas, status_code = venta_controller.get_estadisticas_ventas()
    return jsonify(ventas), status_code


@api.route('/chatbot', methods=['POST'])
def procesar_consulta_chatbot():
    data = request.get_json()
    respuesta = chat_bot_controller.chat_bot(data, datos_ventas=venta_controller.get_estadisticas_ventas())
    return jsonify(respuesta), 200

@api.route('/detalle_venta', methods=['GET'])
def get_all_detalle_ventas():
    detalle_ventas, status_code = venta_detalle_controller.get_all_detalle_ventas()
    return jsonify(detalle_ventas), status_code

@api.route('/detalle_venta/<int:venta_detalle_id>', methods=['GET'])
def get_detalle_venta_by_id(venta_detalle_id):
    detalle_venta, status_code = venta_detalle_controller.get_detalle_venta_by_id(venta_detalle_id)
    return jsonify(detalle_venta), status_code

@api.route('/detalle_venta', methods=['POST'])
def create_detalle_venta():
    data = request.get_json()
    detalle_venta, status_code = venta_detalle_controller.create_detalle_venta(data)
    return jsonify(detalle_venta), status_code

@api.route('/detalle_venta/<int:venta_detalle_id>', methods=['PUT'])
def update_detalle_venta(venta_detalle_id):
    data = request.get_json()
    detalle_venta, status_code = venta_detalle_controller.update_detalle_venta(venta_detalle_id, data)
    return jsonify(detalle_venta), status_code

@api.route('/detalle_venta/<int:venta_detalle_id>', methods=['DELETE'])
def delete_detalle_venta(venta_detalle_id):
    detalle_venta, status_code = venta_detalle_controller.delete_detalle_venta(venta_detalle_id)
    return jsonify(detalle_venta), status_code
