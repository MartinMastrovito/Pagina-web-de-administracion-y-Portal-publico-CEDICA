from flask import Blueprint, request, jsonify
from src.core.crud_pagos import listar_pagos, obtener_pago, crear_pago, actualizar_pago, eliminar_pago

pagos_bp = Blueprint('pagos', __name__, url_prefix='/pagos')

@pagos_bp.route('/', methods=['GET'])
def listar_pagos_route():
    pagos = listar_pagos()
    return jsonify([pago.to_dict() for pago in pagos])

@pagos_bp.route('/<int:id>', methods=['GET'])
def obtener_pago_route(id):
    pago = obtener_pago(id)
    return jsonify(pago.to_dict())

@pagos_bp.route('/', methods=['POST'])
def crear_pago_route():
    data = request.get_json()
    nuevo_pago = crear_pago(data)
    return jsonify(nuevo_pago.to_dict()), 201

@pagos_bp.route('/<int:id>', methods=['PUT'])
def actualizar_pago_route(id):
    data = request.get_json()
    pago = actualizar_pago(id, data)
    return jsonify(pago.to_dict())

@pagos_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_pago_route(id):
    eliminar_pago(id)
    return '', 204