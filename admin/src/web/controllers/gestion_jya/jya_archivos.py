from os import fstat
from flask import render_template, request, send_file, Blueprint
from src.core import crud_JyA
from flask import current_app
from src.core.auth.decorators import login_required, check
from io import BytesIO

bp = Blueprint("documentos", __name__, url_prefix="/JYA/documentos")

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
                "tipo_documento": request.form["tipo"],
        }
        crud_JyA.save_document(**doc_data)
        
    return render_template("JYA/show_jya.html", jya=jya)

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
                "tipo_documento": request.form["tipo"],
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