from flask import Blueprint, request, jsonify
from src.core.auth.models import Empleados
from flask import render_template

empleados_bp = Blueprint('empleados', __name__, url_prefix="/menu_empleados")
@empleados_bp.get("/empleados")
def show_empleado_form():
    return render_template("empleados/menu_empleados.html")

# Creo empleados
@empleados_bp.route('/empleados', methods=['POST'])
def create_empleados():
    data = request.get_json()

    nuevo_empleados = Empleados(
        nombre=data['nombre'],
        apellido=data['apellido'],
        dni=data['dni'],
        domicilio=data['domicilio'],
        email=data['email'],
        localidad=data['localidad'],
        telefono=data['telefono'],
        profesion=data['profesion'],
        puesto=data['puesto'],
        fecha_inicio=data['fecha_inicio'],
        fecha_cese=data.get('fecha_cese', None),
        contacto_emergencia=data['contacto_emergencia'],
        obra_social=data.get('obra_social', ''),
        numero_afiliado=data.get('numero_afiliado', ''),
        condicion=data['condicion'],
        activo=data['activo']
    )

    db.add(nuevo_empleados)
    db.commit()
    return jsonify({'message': 'se creo empleados'})
# Read empleadoss
@empleados_bp.route('/empleados', methods=['GET'])
def list_empleados():
    empleadoss = Empleados.query.all()
    return jsonify([empleados.as_dict() for empleados in empleadoss])

# Update empleados
@empleados_bp.route('/empleados/<int:id>', methods=['PUT'])
def update_empleados(id):
    data = request.get_json()
    empleados = empleados.query.get(id)
    if empleados:
        for key, value in data.items():
            setattr(empleados, key, value)
        db.session.commit()
        return jsonify({'message': 'empleados updated successfully'})
    return jsonify({'message': 'error emple'}), 404

# Delete empleados
@empleados_bp.route('/empleados/<int:id>', methods=['DELETE'])
def delete_empleados(id):
    empleados = empleados.query.get(id)
    if empleados:
        db.session.delete(empleados)
        db.session.commit()
        return jsonify({'message': 'se elimino emple'})
    return jsonify({'message': 'error emple'})
