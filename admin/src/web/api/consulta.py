from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from src.core import crud_consultas as crud_consulta
from src.core.auth.decorators import login_required, check
from datetime import datetime

consulta_api_bp = Blueprint("consulta_api", __name__, url_prefix="/api/consulta")

@consulta_api_bp.route('', methods=['POST'])
def crear_consulta_portal():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    # Imprimir los datos para confirmar qué estamos recibiendo
    print(f"Datos recibidos: {data}")

    nombre_completo = data.get('nombre_completo')
    email = data.get('email')
    mensaje = data.get('mensaje')
    captcha = data.get('captcha')
    estado = data.get('estado')
    fecha = data.get('fecha')

    # Verifica si hay algún campo faltante
    if not nombre_completo or not email or not mensaje or not captcha or not estado or not fecha:
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    # Verifica si el captcha es correcto
    if captcha != "8":
        return jsonify({"error": "Captcha incorrecto"}), 400

    # Procede con la creación de la consulta
    datos_consulta = {
        'nombre_completo': nombre_completo,
        'email': email,
        'fecha': fecha,
        'descripcion': mensaje,
        'estado': estado
    }

    # Verifica si la creación fue exitosa
    nueva_consulta = crud_consulta.create_consulta(**datos_consulta)

    return jsonify({"message": "Consulta guardada correctamente"}), 201
