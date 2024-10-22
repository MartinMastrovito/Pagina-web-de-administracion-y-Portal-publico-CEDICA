from flask import Blueprint, request, render_template, redirect, url_for, flash,jsonify
from src.core.database import db
from src.core.auth.models.model_caballos import Caballo
from src.core.auth.models.model_miembroEquipo import MiembroEquipo
from src.core.auth.models.model_documento import Documento
from src.core.auth.models.model_JyA import JYA
from werkzeug.utils import secure_filename
import os

# Definir el blueprint para caballos
caballos_bp = Blueprint('caballos', __name__)

@caballos_bp.route('/caballos', methods=['GET'])
def menu_caballos():
    page = request.args.get('page', 1, type=int)
    nombre = request.args.get('nombre', '', type=str)
    
    query = db.session.query(Caballo).filter(Caballo.nombre.like(f"%{nombre}%"))
    
    # Ordenar resultados
    orden = request.args.get('orden', 'nombre')
    direction = request.args.get('direction', 'asc')
    
    if direction == 'asc':
        query = query.order_by(getattr(Caballo, orden).asc())
    else:
        query = query.order_by(getattr(Caballo, orden).desc())

    # Paginación
    caballos_paginados = query.paginate(page=page, per_page=10)

    return render_template('caballos/index.html', caballos=caballos_paginados)



@caballos_bp.route('/caballos', methods=['GET'])
def listar_caballos():
    try:
        
        query = db.session.query(Caballo).all()  
        caballos = [
            {
                'id': caballo.id,
                'nombre': caballo.nombre,
                'fecha_nacimiento': caballo.fecha_nacimiento,
                'sexo': caballo.sexo,
                'raza': caballo.raza,
                'pelaje': caballo.pelaje,
                'tipo_ingreso': caballo.tipo_ingreso,
                'fecha_ingreso': caballo.fecha_ingreso,
                'sede_asignada': caballo.sede_asignada,
            }
            for caballo in query
        ]
        return jsonify(caballos), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@caballos_bp.route('/caballos/<int:id>', methods=['GET'])
def mostrar_caballo(id):
    caballo = Caballo.query.get_or_404(id)
    documentos = Documento.query.filter_by(caballo_id=caballo.id).all()  # Obtener documentos del caballo
    return render_template('caballos/show.html', caballo=caballo, documentos=documentos)


@caballos_bp.route('/caballos/nuevo', methods=['GET', 'POST'])
def crear_caballo():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        fecha_nacimiento = request.form['fecha_nacimiento']
        sexo = request.form['sexo']
        raza = request.form['raza']
        pelaje = request.form['pelaje']
        tipo_ingreso = request.form['tipo_ingreso']
        fecha_ingreso = request.form['fecha_ingreso']
        sede_asignada = request.form['sede_asignada']

        # Crear nuevo registro de caballo
        nuevo_caballo = Caballo(
            nombre=nombre,
            fecha_nacimiento=fecha_nacimiento,
            sexo=sexo,
            raza=raza,
            pelaje=pelaje,
            tipo_ingreso=tipo_ingreso,
            fecha_ingreso=fecha_ingreso,
            sede_asignada=sede_asignada
        )
        db.session.add(nuevo_caballo)
        db.session.commit()

        # Manejo de documentos
        documentos = request.files.getlist('documentos')  # Recibe múltiples archivos
        for documento in documentos:
            if documento and documento.filename != '':
                # Guardar el archivo
                filename = secure_filename(documento.filename)
                documento.save(os.path.join('ruta/donde/guardar/documentos', filename))

                # Crear registro del documento
                nuevo_documento = Documento(
                    nombre=documento.filename,
                    tipo_documento='Adjunto',  # Puedes ajustar esto según lo que capture el formulario
                    archivo_url=filename,
                    caballo_id=nuevo_caballo.id
                )
                db.session.add(nuevo_documento)

        db.session.commit()
        flash('Caballo y documentos creados exitosamente.', 'success')
        return redirect(url_for('caballos.listar_caballos'))

    entrenadores = MiembroEquipo.query.all()
    jya_list = JYA.query.all()  
    return render_template('caballos/nuevo.html', entrenadores=entrenadores, JYA=jya_list)


@caballos_bp.route('/caballos/<int:id>/eliminar', methods=['POST'])
def eliminar_caballo(id):
    caballo = Caballo.query.get_or_404(id)
    db.session.delete(caballo)
    db.session.commit()
    flash('Caballo eliminado exitosamente.', 'success')
    return redirect(url_for('caballos.listar_caballos'))


@caballos_bp.route('/caballos/<int:id>/documentos/nuevo', methods=['GET', 'POST'])
def subir_documento(id):
    caballo = Caballo.query.get_or_404(id)

    if request.method == 'POST':
        # Verificar si se ha subido un archivo
        if 'archivo' not in request.files:
            flash('No se ha subido ningún archivo.', 'error')
            return redirect(url_for('caballos.mostrar_caballo', id=caballo.id))

        archivo = request.files['archivo']

        if archivo.filename == '':
            flash('No se ha seleccionado ningún archivo.', 'error')
            return redirect(url_for('caballos.mostrar_caballo', id=caballo.id))

        # Guardar el archivo en el servidor
        archivo_url = f'uploads/{archivo.filename}'  # Define tu ruta para guardar los archivos
        archivo.save(f'src/static/{archivo_url}')  # Asegúrate de que esta ruta sea correcta

        # Crear un nuevo documento y guardarlo en la base de datos
        nuevo_documento = Documento(
            nombre=request.form['nombre'],
            tipo_documento=request.form['tipo_documento'],
            archivo_url=archivo_url,
            caballo_id=caballo.id
        )

        db.session.add(nuevo_documento)
        db.session.commit()

        flash('Documento subido exitosamente.', 'success')
        return redirect(url_for('caballos.mostrar_caballo', id=caballo.id))

    return render_template('caballos/nuevo_documento.html', caballo=caballo)


@caballos_bp.route('/caballos/<int:id>/documentos', methods=['GET'])
def listar_documentos(id):
    caballo = Caballo.query.get_or_404(id)

    # Filtros
    nombre_documento = request.args.get('nombre', '', type=str)
    tipo_documento = request.args.get('tipo', '', type=str)

    # Paginación y ordenación
    page = request.args.get('page', 1, type=int)
    per_page = 10
    orden = request.args.get('orden', 'nombre')
    direction = request.args.get('direction', 'asc')

    # Construir la query con filtros
    query = Documento.query.filter(
        Documento.caballo_id == caballo.id,
        Documento.nombre.like(f"%{nombre_documento}%"),
        Documento.tipo_documento.like(f"%{tipo_documento}%")
    )

    # Ordenar resultados
    if direction == 'asc':
        query = query.order_by(getattr(Documento, orden).asc())
    else:
        query = query.order_by(getattr(Documento, orden).desc())

    # Paginación
    documentos_paginados = query.paginate(page=page, per_page=per_page)

    return render_template('caballos/listar_documentos.html', documentos=documentos_paginados, caballo=caballo, search=nombre_documento)


@caballos_bp.route('/caballos/<int:caballo_id>/documentos/<int:documento_id>/eliminar', methods=['POST'])
def eliminar_documento(caballo_id, documento_id):
    documento = Documento.query.get_or_404(documento_id)
    db.session.delete(documento)
    db.session.commit()
    flash('Documento eliminado exitosamente.', 'success')
    return redirect(url_for('caballos.listar_documentos', id=caballo_id))



@caballos_bp.route('/caballos/<int:id>/editar', methods=['GET', 'POST'])
def editar_caballo(id):
    caballo = Caballo.query.get_or_404(id)

    if request.method == 'POST':
        
        caballo.nombre = request.form['nombre']
        caballo.fecha_nacimiento = request.form['fecha_nacimiento']
        caballo.sexo = request.form['sexo']
        caballo.raza = request.form['raza']
        caballo.pelaje = request.form['pelaje']
        caballo.tipo_ingreso = request.form['tipo_ingreso']
        caballo.fecha_ingreso = request.form['fecha_ingreso']
        caballo.sede_asignada = request.form['sede_asignada']

        db.session.commit()
        flash('Caballo editado exitosamente.', 'success')
        return redirect(url_for('caballos.listar_caballos'))

    return render_template('caballos/editar.html', caballo=caballo)
