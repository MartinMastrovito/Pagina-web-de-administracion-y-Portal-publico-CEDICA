from flask import Blueprint, request, render_template, redirect, url_for, flash
from src.core.crud_caballos import (
    search_caballos, create_caballo, get_caballo_by_id,
    update_caballo, delete_caballo, list_documents, upload_document, delete_document
)
from src.core.auth.models.model_documento import Documento
from src.core.auth.decorators import login_required
from src.core.auth.models.model_miembroEquipo import MiembroEquipo

# Definir el blueprint para caballos
caballos_bp = Blueprint('caballos', __name__, url_prefix='/caballos')

@caballos_bp.route('/', methods=['GET'])
@login_required
def menu_caballos():
    page = request.args.get('page', 1, type=int)
    nombre = request.args.get('nombre', '', type=str)
    tipo_ja_asignado = request.args.get('tipo_ja_asignado', '', type=str)  
    orden = request.args.get('orden', 'nombre')
    direction = request.args.get('direction', 'asc')

    caballos_paginados = search_caballos(nombre=nombre, tipo_ja_asignado=tipo_ja_asignado, sort_by=orden, order=direction, page=page)

    return render_template('caballos/index.html', caballos=caballos_paginados, nombre=nombre, tipo_ja_asignado=tipo_ja_asignado, orden=orden, direction=direction)

@caballos_bp.route('/<int:id>', methods=['GET'])
@login_required
def mostrar_caballo(id):
    caballo = get_caballo_by_id(id)
    documentos = list_documents(caballo_id=caballo.id)
    return render_template('caballos/show.html', caballo=caballo, documentos=documentos)

@caballos_bp.route('/nuevo', methods=['GET', 'POST'])
@login_required
def crear_caballo():
    opciones_ja = ["Hipoterapia", "Monta_Terapéutica", "Deporte_Ecuestre_Adaptado", "Actividades_Recreativas", "Equitación"]
    
    if request.method == 'POST':
        datos_caballo = {
            'nombre': request.form['nombre'],
            'fecha_nacimiento': request.form['fecha_nacimiento'],
            'sexo': request.form['sexo'],
            'raza': request.form['raza'],
            'pelaje': request.form['pelaje'],
            'tipo_ingreso': request.form['tipo_ingreso'],
            'fecha_ingreso': request.form['fecha_ingreso'],
            'sede_asignada': request.form['sede_asignada'],
            'tipo_ja_asignado_asignado': request.form.getlist('tipo_ja_asignado_asignado')  # Recoge la selección
        }
        datos_caballo['tipo_ja_asignado_asignado'] = ', '.join(datos_caballo['tipo_ja_asignado_asignado'])  # Convierte la lista a string
        nuevo_caballo = create_caballo(**datos_caballo)
        flash('Caballo creado exitosamente.', 'success')
        return redirect(url_for('caballos.menu_caballos'))
    
    return render_template('caballos/nuevo.html', opciones_ja=opciones_ja)

@caballos_bp.route('/<int:id>/eliminar', methods=['POST'])
@login_required
def eliminar_caballo(id):
    delete_caballo(id)
    flash('Caballo eliminado exitosamente.', 'success')
    return redirect(url_for('caballos.menu_caballos'))

@caballos_bp.route('/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_caballo(id):
    caballo = get_caballo_by_id(id)
    if request.method == 'POST':
        datos_actualizados = {
            'nombre': request.form['nombre'],
            'fecha_nacimiento': request.form['fecha_nacimiento'],
            'sexo': request.form['sexo'],
            'raza': request.form['raza'],
            'pelaje': request.form['pelaje'],
            'tipo_ingreso': request.form['tipo_ingreso'],
            'fecha_ingreso': request.form['fecha_ingreso'],
            'sede_asignada': request.form['sede_asignada'],
        }
        update_caballo(id, **datos_actualizados)
        flash('Caballo editado exitosamente.', 'success')
        return redirect(url_for('caballos.menu_caballos'))
    return render_template('caballos/editar.html', caballo=caballo)

@caballos_bp.route('/<int:id>/documentos/nuevo', methods=['GET', 'POST'])
@login_required
def subir_documento(id):
    if request.method == 'POST':
        if 'archivo' not in request.files:
            flash('No se ha subido ningún archivo.', 'error')
            return redirect(url_for('caballos.mostrar_caballo', id=id))

        archivo = request.files['archivo']
        if archivo.filename == '':
            flash('No se ha seleccionado ningún archivo.', 'error')
            return redirect(url_for('caballos.mostrar_caballo', id=id))

        nombre_documento = request.form['nombre']
        tipo_documento = request.form['tipo_documento']
        
        # Usar MinIO para subir el archivo
        upload_document(id, archivo, nombre_documento, tipo_documento)
        flash('Documento subido exitosamente.', 'success')
        return redirect(url_for('caballos.mostrar_caballo', id=id))

    return render_template('caballos/nuevo_documento.html', caballo=get_caballo_by_id(id))

@caballos_bp.route('/<int:caballo_id>/documentos/<int:documento_id>/eliminar', methods=['POST'])
@login_required
def eliminar_documento(caballo_id, documento_id):
    delete_document(documento_id)
    flash('Documento eliminado exitosamente.', 'success')
    return redirect(url_for('caballos.mostrar_caballo', id=caballo_id))
