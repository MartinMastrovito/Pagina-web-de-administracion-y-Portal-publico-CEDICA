from os import fstat
from flask import render_template, request, redirect, flash, send_file
from flask import Blueprint
from core import crud_JyA
from flask import current_app
from core.auth.decorators import login_required  # Importamos el decorador
from core.auth.decorators import check  # Importamos el decorador
from io import BytesIO

bp = Blueprint("crud_JyA", __name__, url_prefix="/JYA")

@bp.get("/")
@login_required
@check("jya_index")
def index():
    nombre = request.args.get('nombre')
    apellido = request.args.get('apellido')
    dni = request.args.get('dni', type=int)
    profesionales_atendiendo = request.args.get("profesionales_atendiendo")
    sort_by = request.args.get('sort_by', 'nombre')  # Cambié 'email' a 'nombre' para evitar errores
    order = request.args.get('order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = 25

    # Obtener resultados paginados usando la búsqueda
    users_pagination = crud_JyA.search_JYA(
        nombre=nombre,
        apellido=apellido,
        dni=dni,
        profesionales_atendiendo=profesionales_atendiendo,
        sort_by=sort_by,
        order=order,
        page=page,
        per_page=per_page
    )

    # Renderizar la plantilla con la lista de JYA y la paginación
    return render_template(
        "JYA/list_jya.html",
        jyas=users_pagination.items,  # Lista de usuarios (jya) para el template
        pagination=users_pagination    # Objeto de paginación para usar en la navegación
    )
    
@bp.get("/crear_jya")
@login_required
@check("jya_new")
def show_create_jya_form():
    return render_template("JYA/create_jya.html")

@bp.post("/crear_jya")
@login_required
@check("jya_new")
def create_jya():
    jya_data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "dni": request.form['dni'],
        "edad": request.form["edad"],
        "fecha_nacimiento": request.form["fecha_de_nacimiento"],
        "lugar_nacimiento": {
            "localidad": request.form["lugar_nacimiento_localidad"],
            "provincia": request.form["lugar_nacimiento_provincia"]
        },
        "domicilio_actual": {
            "calle": request.form["domicilio_actual_calle"],
            "numero": request.form["domicilio_actual_numero"],
            "departamento": request.form.get("domicilio_actual_departamento", ""),
            "localidad": request.form["domicilio_actual_localidad"],
            "provincia": request.form["domicilio_actual_provincia"]
        },
        "telefono_actual": request.form["telefono_actual"],
        "contacto_emergencia": {
            "nombre": request.form["contacto_emergencia_nombre"],
            "telefono": request.form["contacto_emergencia_telefono"]
        },
        "becado": request.form["becado"] == "true",
        "porcentaje_beca": float(request.form["porcentaje_beca"] or 0.0),
        "profesionales_atendiendo": request.form["profesionales_atendiendo"],
    }

    user = crud_JyA.create_jya(**jya_data)
    
    if user:
        flash('Usuario creado exitosamente', 'success')
        return redirect('/JYA')
    else:
        flash('El usuario ya existe o ocurrió un error', 'danger')
        return redirect('/JYA/crear_jya')

@bp.get("documentos/cargar_documentos/<int:jya_dni>")
@login_required
@check("jya_new")
def show_upload_document(jya_dni):
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    return render_template("JYA/upload_document.html", jya=jya)

@bp.post("documentos/cargar_documentos/<int:jya_dni>")
@login_required
@check("jya_new")
def upload_document(jya_dni):
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    if "documento" in request.files:
        file = request.files["documento"]
        client = current_app.storage.client
        size = fstat(file.fileno()).st_size
        
        client.put_object(
            "grupo30",
            f"documentos-JYA/{file.filename}",
            file,
            size,
            content_type=file.content_type
        )
        
        doc_data = {"jya_dni":jya_dni,
                "nombre_documento":f"documentos-JYA/{file.filename}",
                "tipo": request.form["tipo"],
        }
        crud_JyA.save_document(**doc_data)
        
    return render_template("JYA/show_jya.html", jya=jya)

def upload_minio_document(file):
    if file:
        client = current_app.storage.client
        size = fstat(file.fileno()).st_size
        
        client.put_object(
            "grupo30",
            f"documentos-JYA/{file.filename}",
            file,
            size,
            content_type=file.content_type
        )
        
        return f"documentos-JYA/{file.filename}"
    return None
    
@bp.get("/actualizar/<int:jya_dni>")
@login_required
@check("jya_update")
def show_update_jya(jya_dni):
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    return render_template("JYA/update_jya.html", jya=jya)

@bp.post("/actualizar/<int:jya_dni>")
@login_required
@check("jya_update")
def jya_update(jya_dni):
    jya_data = {
        "nombre": request.form['nombre'],
        "apellido": request.form['apellido'],
        "dni": request.form['dni'],
        "edad": request.form["edad"],
        "fecha_nacimiento": request.form["fecha_de_nacimiento"],
        "lugar_nacimiento": {
            "localidad": request.form["lugar_nacimiento_localidad"],
            "provincia": request.form["lugar_nacimiento_provincia"]
        },
        "domicilio_actual": {
            "calle": request.form["domicilio_actual_calle"],
            "numero": request.form["domicilio_actual_numero"],
            "departamento": request.form.get("domicilio_actual_departamento", ""),
            "localidad": request.form["domicilio_actual_localidad"],
            "provincia": request.form["domicilio_actual_provincia"]
        },
        "telefono_actual": request.form["telefono_actual"],
        "contacto_emergencia": {
            "nombre": request.form["contacto_emergencia_nombre"],
            "telefono": request.form["contacto_emergencia_telefono"]
        },
        "becado": request.form["becado"] == "true",
        "porcentaje_beca": float(request.form["porcentaje_beca"] or 0.0),
        "profesionales_atendiendo": request.form["profesionales_atendiendo"],
    }
    crud_JyA.update_jya(jya_dni, **jya_data)
    
    return redirect('/JYA')

@bp.get("/eliminar/<int:jya_dni>")
@login_required
@check("jya_destroy")
def show_delete_jya(jya_dni):
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    return render_template("JYA/delete_jya.html", jya=jya)

@bp.post("/eliminar/<int:jya_dni>")
@login_required
@check("jya_destroy")
def jya_delete(jya_dni):
    crud_JyA.delete_jya(jya_dni)
    return redirect('/JYA')

@bp.get("/detalles/<int:jya_dni>")
@login_required
@check("jya_show")
def show_details_jya(jya_dni):
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    return render_template("JYA/show_jya.html", jya=jya)

@bp.get("/documentos/<int:jya_dni>")
@login_required
@check("jya_show")
def index_documents_jya(jya_dni):
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    # Obtener parámetros de búsqueda y ordenamiento
    nombre_documento = request.args.get('nombre_documento')
    tipo_documento = request.args.get('tipo_documento')
    sort_by = request.args.get('sort_by', 'nombre_documento')  # Campo por defecto para ordenar
    order = request.args.get('order', 'asc')  # Orden por defecto
    page = request.args.get('page', 1, type=int)  # Página actual
    per_page = 10  # Elementos por página

    # Filtrar y paginar documentos
    documentos_pagination = crud_JyA.search_documents(
        jya_dni=jya_dni,
        nombre_documento=nombre_documento,
        tipo_documento=tipo_documento,
        sort_by=sort_by,
        order=order,
        page=page,
        per_page=per_page
    )

    return render_template("JYA/show_documents_jya.html", jya=jya, documentos=documentos_pagination.items, pagination=documentos_pagination)


@bp.get("/documentos/actualizar/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_update")
def show_update_document_jya(jya_dni, documento_id):
    documento = crud_JyA.get_document_by_id(documento_id)
    jya = crud_JyA.get_jya_by_document(documento)
    
    return render_template("JYA/edit_document_jya.html", jya=jya, documento=documento)

@bp.post("/documentos/actualizar/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_update")
def update_document_jya(jya_dni, documento_id):
    documento = crud_JyA.get_document_by_id(documento_id)
    
    if "documento" in request.files:
        
        client = current_app.storage.client
        client.remove_object('grupo30', documento.nombre_documento)
        
        file = request.files["documento"]
        size = fstat(file.fileno()).st_size
        
        client.put_object(
            "grupo30",
            f"documentos-JYA/{file.filename}",
            file,
            size,
            content_type=file.content_type
        )
        
        doc_data = {
                "nombre_documento":f"documentos-JYA/{file.filename}",
                "tipo": request.form["tipo"],
        }
        
        crud_JyA.update_document(documento.id, **doc_data)
    
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    return render_template("JYA/show_jya.html", jya=jya)

@bp.get("/documentos/eliminar/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_destroy")
def show_delete_document_jya(jya_dni, documento_id):
    documento = crud_JyA.get_document_by_id(documento_id)
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    return render_template("JYA/delete_document_jya.html", jya=jya, documento=documento)

@bp.post("/documentos/eliminar/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_destroy")
def delete_document_jya(jya_dni, documento_id):
    documento = crud_JyA.get_document_by_id(documento_id)
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    client = current_app.storage.client
    client.remove_object('grupo30', documento.nombre_documento)
    
    crud_JyA.delete_document(documento.id)
    
    return render_template("JYA/show_jya.html", jya=jya)

@bp.get("/documentos/descargar/<int:documento_id>")
@login_required
@check("jya_new")  # Asegúrate de tener el control de acceso adecuado
def download_documento(documento_id):
    documento = crud_JyA.get_document_by_id(documento_id)
    
    client = current_app.storage.client  # Asumiendo que tienes el cliente configurado
    bucket_name = 'grupo30'
    file_name = documento.nombre_documento

    # Obtener el objeto desde MinIO
    data = client.get_object(bucket_name, file_name)

    # Leer el objeto en memoria
    file_data = BytesIO(data.read())
    file_data.seek(0)  # Rewind para asegurarnos de que se lea desde el principio

    # Devolver el archivo como una respuesta
    return send_file(file_data, as_attachment=True, download_name=documento.nombre_documento)