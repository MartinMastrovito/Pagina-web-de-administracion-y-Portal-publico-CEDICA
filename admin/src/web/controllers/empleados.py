from flask import Blueprint, request, jsonify, url_for
from src.core.auth.models.model_empleado import Empleados
from flask import render_template , flash, redirect, current_app
from src.core.database import db
from core.auth.decorators import login_required 
from werkzeug.utils import secure_filename
from sqlalchemy import asc, desc
import os

empleados_bp = Blueprint('empleados', __name__, url_prefix="/menu_empleados", template_folder='../templates/empleados',static_folder="/admin/static")
@empleados_bp.get("/empleados")

def show_empleado_form():
    return render_template("/empleados/menu_empleados.html")

#crear empleados

@empleados_bp.get("/crear_empleado")
def crear_empleado():
    return render_template("/empleados/crear_empleado.html")

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
            file = request.files["documentacion"]
            client = current_app.storage.client
            size = os.fstat(file.fileno()).st_size
            
            client.put_object(
                "grupo30",
                f"documentos-Emple/{file.filename}",
                file,
                size,
                content_type=file.content_type
            )
        return redirect("/menu_empleados/crear_empleado")




    except Exception as e:
        db.session.rollback()
        flash('Ocurrió un error al crear el empleado: ' + str(e), 'danger')
        return redirect("/menu_empleados/crear_empleado")





# listar empleados
@empleados_bp.route('/listar_empleados', methods=['GET'])
def listar_empleados():
    nombre = request.args.get('nombre')  
    apellido = request.args.get('apellido')
    dni = request.args.get('dni')
    puesto = request.args.get('puesto')
    ordenar_por = request.args.get('ordenar_por', 'nombre')  
    direccion_orden = request.args.get('direccion_orden', 'asc') 
    query = db.session.query(Empleados)

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
@empleados_bp.route('/empleados/<int:id>', methods=['POST','PUT'])
def actualizar_empleados(id):
    empleado = Empleados.query.get(id)
    
    if empleado:
        data = request.get_json()
        for key, value in data.items():
            setattr(empleado, key, value)
        db.session.commit()
        jsonify({'message': 'Empleado actualizado exitosamente'}), 200
        return redirect(url_for('empleados.listar_empleados'))
    jsonify({'message': 'Empleado no encontrado'}), 404
    return redirect(url_for('empleados.listar_empleados'))


# eliminar empleados
@empleados_bp.route('/empleados/<int:id>', methods=['DELETE', 'POST'])
def eliminar_empleados(id):
    empleados = Empleados.query.get(id)
    if empleados:
        db.session.delete(empleados)
        db.session.commit()
        jsonify({'message': 'se elimino emple'})
        return redirect(url_for('empleados.listar_empleados'))
    jsonify({'message': 'error emple'})
    return redirect(url_for('empleados.listar_empleados'))
