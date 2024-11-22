import requests
from flask import Blueprint, jsonify, request
from src.core import crud_consultas as crud_consulta

consulta_api_bp = Blueprint("consulta_api", __name__, url_prefix="/api/consulta")

# Tu clave secreta de reCAPTCHA
RECAPTCHA_SECRET_KEY = "6LfMIYYqAAAAAG9SdB6g7AfOJaALFZVDfl37N2ci"

@consulta_api_bp.route('', methods=['POST'])
def crear_consulta_portal():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No se enviaron datos"}), 400

    nombre_completo = data.get('nombre_completo')
    email = data.get('email')
    mensaje = data.get('mensaje')
    captcha = data.get('captcha')  # Token de reCAPTCHA
    estado = data.get('estado')
    fecha = data.get('fecha')

    if not all([nombre_completo, email, mensaje, captcha, estado, fecha]):
        return jsonify({"error": "Faltan campos obligatorios"}), 400

    # Verificar el token de reCAPTCHA
    recaptcha_response = requests.post(
        "https://www.google.com/recaptcha/api/siteverify",
        data={
            "secret": RECAPTCHA_SECRET_KEY,
            "response": captcha,
        },
    )

    recaptcha_result = recaptcha_response.json()
    if not recaptcha_result.get("success"):
        return jsonify({"error": "Captcha inválido"}), 400

    # Proceder con la creación de la consulta
    datos_consulta = {
        "nombre_completo": nombre_completo,
        "email": email,
        "fecha": fecha,
        "descripcion": mensaje,
        "estado": estado,
    }
    nueva_consulta = crud_consulta.create_consulta(**datos_consulta)

    return jsonify({"message": "Consulta guardada correctamente"}), 201
