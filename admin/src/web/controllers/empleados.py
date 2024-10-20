from flask import Blueprint, request, jsonify
from src.core.auth.models import Empleados
from flask import render_template
from src.core.database import db
from sqlalchemy import asc, desc

empleados_bp = Blueprint('empleados', __name__, url_prefix="/menu_empleados", template_folder='../templates/empleados',static_folder="/admin/static")
@empleados_bp.get("/empleados")

def show_empleado_form():
    return render_template("empleados/menu_empleados.html")

#crear empleados

@empleados_bp.get("/crear-empleado")
def crear_empleado():
    return render_template("empleados/crear_empleado.html")


# listar empleados
@empleados_bp.route('/lista-empleados', methods=['GET'])
def listar_empleados():
    nombre = request.args.get('nombre')  
    apellido = request.args.get('apellido')
    dni = request.args.get('dni')
    puesto = request.args.get('puesto')
    ordenar_por = request.args.get('ordenar_por', 'nombre')  
    direccion_orden = request.args.get('direccion_orden', 'asc') 
    query = db.query.all(Empleados)

    if nombre:
        query = query.filter(Empleados.nombre.ilike(f'%{nombre}%')) #realiza busquedas insensibles a mayusculas y minuscula
    if apellido:
        query = query.filter(Empleados.apellido.ilike(f'%{apellido}%'))
    if dni:
        query = query.filter(Empleados.dni == dni)
    if puesto:
        query = query.filter(Empleados.puesto.ilike(f'%{puesto}%'))

    if direccion_orden == 'asc':
        query = query.order_by(asc(getattr(Empleados, ordenar_por)))
    else:
        query = query.order_by(desc(getattr(Empleados, ordenar_por)))

    empleados = query.all()
    return render_template('empleados/listar_empleados.html', empleados=empleados)


# actualizar empleados
@empleados_bp.route('/empleados/<int:id>', methods=['PUT'])
def actualizar_empleados(id):
    empleado = Empleados.query.get(id)
    
    if empleado:
        data = request.get_json()
        for key, value in data.items():
            setattr(empleado, key, value)
        db.session.commit()
        return jsonify({'message': 'Empleado actualizado exitosamente'}), 200
    return jsonify({'message': 'Empleado no encontrado'}), 404


# eliminar empleados
@empleados_bp.route('/empleados/<int:id>', methods=['DELETE'])
def eliminar_empleados(id):
    empleados = empleados.query.get(id)
    if empleados:
        db.session.delete(empleados)
        db.session.commit()
        return jsonify({'message': 'se elimino emple'})
    return jsonify({'message': 'error emple'})
