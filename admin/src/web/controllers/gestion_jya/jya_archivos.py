from os import fstat
from flask import render_template, request, send_file, Blueprint, current_app, flash, redirect
from src.core import crud_JyA
from src.core.auth.decorators import login_required, check
from io import BytesIO

bp = Blueprint("documentos", __name__, url_prefix="/JYA/documentos")

@bp.get("/<int:jya_dni>")
@login_required
@check("jya_show")
def index_documents_jya(jya_dni):
    """
    Muestra la lista de documentos asociados a un JYA específico, 
    con opciones de búsqueda y ordenamiento.

    Args:
        jya_dni: DNI del JYA cuyos documentos se listan.

    Returns:
        Renderizado de la plantilla show_documents_jya.html con los documentos y paginación.
    """
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    nombre_documento = request.args.get("nombre_documento")
    tipo_documento = request.args.get("tipo_documento")
    sort_by = request.args.get("sort_by", "nombre_documento")
    order = request.args.get("order", "asc")
    page = request.args.get("page", 1, type=int)
    per_page = 10

    documentos_pagination = crud_JyA.search_documents(
        jya_dni=jya_dni,
        nombre_documento=nombre_documento,
        tipo_documento=tipo_documento,
        sort_by=sort_by,
        order=order,
        page=page,
        per_page=per_page
    )

    for documento in documentos_pagination.items:
        documento.nombre_documento = documento.nombre_documento[documento.nombre_documento.find("=")+1:]
    
    return render_template(
        "JYA/show_documents_jya.html",
        jya=jya,
        documentos=documentos_pagination.items,
        pagination=documentos_pagination
    )

@bp.get("/cargar_documentos/<int:jya_dni>")
@login_required
@check("jya_new")
def show_upload_document(jya_dni):
    """
    Muestra el formulario para cargar un nuevo documento asociado a un JYA.

    Args:
        jya_dni: DNI del JYA para el cual se carga el documento.

    Returns:
        Renderizado de la plantilla upload_document.html.
    """
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    return render_template("JYA/upload_document.html", jya=jya)

@bp.post("/cargar_documentos/<int:jya_dni>")
@login_required
@check("jya_new")
def upload_document(jya_dni):
    """
    Carga un documento asociado a un JYA en el almacenamiento y lo guarda en la base de datos.

    Args:
        jya_dni: DNI del JYA para el cual se carga el documento.

    Returns:
        Renderizado de la plantilla show_jya.html después de cargar el documento.
    """
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    if "documento" in request.files:
        file = request.files["documento"]
        if file.filename.lower().endswith(('.pdf', '.doc', '.xls', '.jpeg')):
            client = current_app.storage.client
            size = fstat(file.fileno()).st_size
            
            client.put_object(
                "grupo30",
                f"documentos-JYA/{jya_dni}/{crud_JyA.cant_documentos()}={file.filename}",
                file,
                size,
                content_type=file.content_type
            )
            
            doc_data = {
                "jya_dni": jya_dni,
                "nombre_documento": f"documentos-JYA/{jya_dni}/{crud_JyA.cant_documentos()}={file.filename}",
                "tipo_documento": request.form["tipo"]
            }
            crud_JyA.save_document(**doc_data)
    
            flash('Se ha subido el archivo exitosamente!', 'success')
        else:
            flash('No se pudo subir el archivo! Verifique que esté intentando subir un archivo de tipo .pdf, .doc, .xls o .jpeg', 'danger')
            
    return redirect(f"/JYA/documentos/{jya_dni}")

@bp.get("/actualizar/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_update")
def show_update_document_jya(jya_dni, documento_id):
    """
    Muestra el formulario para actualizar un documento específico de un JYA.

    Args:
        jya_dni: DNI del JYA al que pertenece el documento.
        documento_id: ID del documento a actualizar.

    Returns:
        Renderizado de la plantilla edit_document_jya.html.
    """
    documento = crud_JyA.get_document_by_id(documento_id)
    jya = crud_JyA.get_jya_by_document(documento)
    
    return render_template("JYA/edit_document_jya.html", jya=jya, documento=documento)

@bp.post("/actualizar/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_update")
def update_document_jya(jya_dni, documento_id):
    """
    Actualiza un documento de un JYA, reemplazándolo en el almacenamiento 
    y actualizando la base de datos.

    Args:
        jya_dni: DNI del JYA al que pertenece el documento.
        documento_id: ID del documento a actualizar.

    Returns:
        Renderizado de la plantilla show_jya.html después de actualizar el documento.
    """
    documento = crud_JyA.get_document_by_id(documento_id)
    
    if "documento" in request.files:
        file = request.files["documento"]
        if file.filename.lower().endswith(('.pdf', '.doc', '.xls', '.jpeg')):
            client = current_app.storage.client
            client.remove_object("grupo30", documento.nombre_documento)
            
            size = fstat(file.fileno()).st_size
            
            client.put_object(
                "grupo30",
                f"documentos-JYA/{jya_dni}/{crud_JyA.cant_documentos()}={file.filename}",
                file,
                size,
                content_type=file.content_type
            )
            
            doc_data = {
                "nombre_documento": f"documentos-JYA/{jya_dni}/{crud_JyA.cant_documentos()}={file.filename}",
                "tipo_documento": request.form["tipo"]
            }
            crud_JyA.update_document(documento.id, **doc_data)
            
            flash('Se ha actualizado el archivo exitosamente!', 'success')
        else:
            flash('No se pudo actualizar el archivo! Verifique que esté intentando subir un archivo de tipo .pdf, .doc, .xls o .jpeg', 'danger')
    
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    
    return redirect(f"/JYA/documentos/{jya_dni}")

@bp.get("/eliminar/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_destroy")
def show_delete_document_jya(jya_dni, documento_id):
    """
    Muestra la confirmación para eliminar un documento específico de un JYA.

    Args:
        jya_dni: DNI del JYA al que pertenece el documento.
        documento_id: ID del documento a eliminar.

    Returns:
       Renderizado de la plantilla delete_document_jya.html.
    """
    documento = crud_JyA.get_document_by_id(documento_id)
    documento.nombre_documento = documento.nombre_documento[documento.nombre_documento.find("=")+1:]
    
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    return render_template("JYA/delete_document_jya.html", jya=jya, documento=documento)

@bp.post("/eliminar/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_destroy")
def delete_document_jya(jya_dni, documento_id):
    """
    Elimina un documento de un JYA tanto del almacenamiento como de la base de datos.

    Args:
        jya_dni: DNI del JYA al que pertenece el documento.
        documento_id: ID del documento a eliminar.

    Returns:
        Renderizado de la plantilla show_jya.html después de la eliminación.
    """
    documento = crud_JyA.get_document_by_id(documento_id)
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    client = current_app.storage.client
    client.remove_object("grupo30", documento.nombre_documento)
    
    crud_JyA.delete_document(documento.id)
    
    flash('Se ha eliminado el archivo exitosamente!', 'success')
    return redirect(f"/JYA/documentos/{jya_dni}")

@bp.get("/descargar/<int:documento_id>")
@login_required
@check("jya_show")
def download_documento(documento_id):
    """
    Permite la descarga de un documento específico asociado a un JYA.

    Args:
        documento_id): ID del documento a descargar.

    Returns:
        Archivo descargable con los datos del documento.
    """
    documento = crud_JyA.get_document_by_id(documento_id)
    client = current_app.storage.client
    bucket_name = "grupo30"
    file_name = documento.nombre_documento

    data = client.get_object(bucket_name, file_name)
    file_data = BytesIO(data.read())
    file_data.seek(0)

    return send_file(file_data, as_attachment=True, download_name=documento.nombre_documento)
