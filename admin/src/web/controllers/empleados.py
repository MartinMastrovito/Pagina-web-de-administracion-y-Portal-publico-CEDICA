from flask import Blueprint, request, jsonify
from src.core.auth.models import Empleados
from flask import render_template

empleados_bp = Blueprint('empleados', __name__, url_prefix="/menu_empleados", template_folder='../templates/empleados',static_folder="/admin/static")
@empleados_bp.get("/empleados")
def show_empleado_form():
    return render_template("empleados/menu_empleados.html")

# regreso al menu emple
def empleado_menu():
    return render_template("menu_empleados.html",empleados=empleados_bp)

@empleados_bp.get("/crear-empleado")
def crear_empleado():
    return render_template("empleados/crear_empleado.html")

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
