from flask import Blueprint, request, jsonify
from src.core.auth.models import Empleados
from flask import render_template , flash, redirect, current_app
from src.core.database import db
from sqlalchemy import asc, desc
from core.auth.decorators import login_required 
from werkzeug.utils import secure_filename
import os

empleados_bp = Blueprint('empleados', __name__, url_prefix="/menu_empleados", template_folder='../templates/empleados',static_folder="/admin/static")
@empleados_bp.get("/empleados")

def show_empleado_form():
    return render_template("empleados/menu_empleados.html")

#crear empleados

@empleados_bp.get("/crear-empleado")
def crear_empleado():
    return render_template("empleados/crear_empleado.html")

@empleados_bp.post("/crear_empleado")
@login_required
def crear_empleado_listo():
    # Obtener los datos del formulario
    empleado_data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "dni": request.form['dni'],
        "domicilio": request.form['domicilio'],
        "email": request.form['email'],
        "localidad": request.form['localidad'],
        "telefono": request.form['telefono'],
        "profesion": request.form['profesion'],
        "puesto": request.form['puesto'],
        "fecha_inicio": request.form['fecha_inicio'],
        "fecha_cese": request.form.get('fecha_cese'),  # Puede ser None si no se proporciona
        "contacto_emergencia": request.form['contacto_emergencia'],
        "obra_social": request.form.get('obra_social'),  # Opcional
        "numero_afiliado": request.form.get('numero_afiliado'),  # Opcional
        "condicion": request.form['condicion'],
        "activo": True if request.form['activo'] == 'true' else False
    }

    # Crear instancia de empleado
    nuevo_empleado = Empleados(**empleado_data)

    # Guardar el empleado en la base de datos
    try:
        db.session.add(nuevo_empleado)
        db.session.commit()
        flash('Empleado creado exitosamente', 'success')

        # Si se subieron archivos
        if 'documentacion' in request.files:
            files = request.files.getlist('documentacion')
            for file in files:
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    # Aquí puedes agregar lógica para guardar la referencia del archivo en la BD si es necesario.
        
        return redirect('/menu_empleados/empleados')


    except Exception as e:
        db.session.rollback()
        flash('Ocurrió un error al crear el empleado: ' + str(e), 'danger')
        return redirect("/empleados/crear_empleado")




# listar empleados
@empleados_bp.route('/lista-empleados', methods=['GET'])
def listar_empleados():
    nombre = request.args.get('nombre')  
    apellido = request.args.get('apellido')
    dni = request.args.get('dni')
    puesto = request.args.get('puesto')
    ordenar_por = request.args.get('ordenar_por', 'nombre')  
    direccion_orden = request.args.get('direccion_orden', 'asc') 
    query = db.query(Empleados)

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
