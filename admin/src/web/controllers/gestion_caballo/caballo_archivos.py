from os import fstat
from flask import render_template, request, send_file, Blueprint, current_app
from src.core import crud_caballos as crud_caballo
from src.core.auth.decorators import login_required, check
from io import BytesIO

caballos_documentos_bp = Blueprint("caballos_documentos", __name__, url_prefix="/caballos/documentos")

@caballos_documentos_bp.get("/<int:caballo_id>")
@login_required
@check("horse_index")
def index_documents_caballo(caballo_id):
    """
    Muestra la lista de documentos asociados a un caballo específico, 
    con opciones de búsqueda y ordenamiento.

    Args:
        caballo_id: ID del caballo cuyos documentos se listan.

    Returns:
        Renderizado de la plantilla show_documents_caballo.html con los documentos y paginación.
    """
    caballo = crud_caballo.get_caballo_by_id(caballo_id)
    nombre_documento = request.args.get("nombre_documento")
    tipo_documento = request.args.get("tipo_documento")
    sort_by = request.args.get("sort_by", "nombre_documento")
    order = request.args.get("order", "asc")
    page = request.args.get("page", 1, type=int)
    per_page = 10

    documentos_pagination = crud_caballo.list_documents(
        caballo_id=caballo_id,
        nombre_documento=nombre_documento,
        tipo_documento=tipo_documento,
        sort_by=sort_by,
        order=order,
        page=page,
        per_page=per_page
    )

    return render_template(
        "caballos/show_documents_caballo.html",
        caballo=caballo,
        documentos=documentos_pagination.items,
        pagination=documentos_pagination
    )

@caballos_documentos_bp.get("/documentos/cargar_documentos/<int:caballo_id>")
@login_required
@check("horse_new")
def show_upload_document(caballo_id):
    """
    Muestra el formulario para cargar un nuevo documento asociado a un caballo.

    Args:
        caballo_id: ID del caballo para el cual se carga el documento.

    Returns:
        Renderizado de la plantilla upload_document.html.
    """
    caballo = crud_caballo.get_caballo_by_id(caballo_id)
    return render_template("caballos/upload_document.html", caballo=caballo)

@caballos_documentos_bp.post("/documentos/cargar_documentos/<int:caballo_id>")
@login_required
@check("horse_new")
def upload_document(caballo_id):
    """
    Carga un documento asociado a un caballo en el almacenamiento y lo guarda en la base de datos.

    Args:
        caballo_id: ID del caballo para el cual se carga el documento.

    Returns:
        Renderizado de la plantilla show_caballo.html después de cargar el documento.
    """
    caballo = crud_caballo.get_caballo_by_id(caballo_id)
    
    if "documento" in request.files:
        file = request.files["documento"]
        client = current_app.storage.client
        size = fstat(file.fileno()).st_size
        
        client.put_object(
            "grupo30",
            f"documentos-caballo/{file.filename}",
            file,
            size,
            content_type=file.content_type
        )
        
        doc_data = {
            "caballo_id": caballo_id,
            "nombre_documento": f"documentos-caballo/{file.filename}",
            "tipo_documento": request.form["tipo"]
        }
        crud_caballo.save_document(**doc_data)
        
    return render_template("caballos/show.html", caballo=caballo)

@caballos_documentos_bp.get("/documentos/actualizar/<int:caballo_id>/<int:documento_id>")
@login_required
@check("horse_update")
def show_update_document_caballo(caballo_id, documento_id):
    """
    Muestra el formulario para actualizar un documento específico de un caballo.

    Args:
        caballo_id: ID del caballo al que pertenece el documento.
        documento_id: ID del documento a actualizar.

    Returns:
        Renderizado de la plantilla edit_document_caballo.html.
    """
    documento = crud_caballo.get_document_by_id(documento_id)
    caballo = crud_caballo.get_caballo_by_document(documento)
    
    return render_template("caballos/edit_document_caballo.html", caballo=caballo, documento=documento)

@caballos_documentos_bp.post("/documentos/actualizar/<int:caballo_id>/<int:documento_id>")
@login_required
@check("horse_update")
def update_document_caballo(caballo_id, documento_id):
    """
    Actualiza un documento de un caballo, reemplazándolo en el almacenamiento 
    y actualizando la base de datos.

    Args:
        caballo_id: ID del caballo al que pertenece el documento.
        documento_id: ID del documento a actualizar.

    Returns:
        Renderizado de la plantilla show_caballo.html después de actualizar el documento.
    """
    documento = crud_caballo.get_document_by_id(documento_id)
    
    if "documento" in request.files:
        client = current_app.storage.client
        client.remove_object("grupo30", documento.nombre_documento)
        
        file = request.files["documento"]
        size = fstat(file.fileno()).st_size
        
        client.put_object(
            "grupo30",
            f"documentos-caballo/{file.filename}",
            file,
            size,
            content_type=file.content_type
        )
        
        doc_data = {
            "nombre_documento": f"documentos-caballo/{file.filename}",
            "tipo_documento": request.form["tipo"]
        }
        crud_caballo.update_document(documento.id, **doc_data)
    
    caballo = crud_caballo.get_caballo_by_id(caballo_id)
    
    return render_template("caballos/show.html", caballo=caballo)

@caballos_documentos_bp.get("/documentos/eliminar/<int:caballo_id>/<int:documento_id>")
@login_required
@check("horse_destroy")
def show_delete_document_caballo(caballo_id, documento_id):
    """
    Muestra la confirmación para eliminar un documento específico de un caballo.

    Args:
        caballo_id: ID del caballo al que pertenece el documento.
        documento_id: ID del documento a eliminar.

    Returns:
       Renderizado de la plantilla delete_document_caballo.html.
    """
    documento = crud_caballo.get_document_by_id(documento_id)
    caballo = crud_caballo.get_caballo_by_id(caballo_id)
    
    return render_template("caballos/delete_document_caballo.html", caballo=caballo, documento=documento)

@caballos_documentos_bp.post("/documentos/eliminar/<int:caballo_id>/<int:documento_id>")
@login_required
@check("horse_destroy")
def delete_document_caballo(caballo_id, documento_id):
    """
    Elimina un documento de un caballo tanto del almacenamiento como de la base de datos.

    Args:
        caballo_id: ID del caballo al que pertenece el documento.
        documento_id: ID del documento a eliminar.

    Returns:
        Renderizado de la plantilla show_caballo.html después de la eliminación.
    """
    documento = crud_caballo.get_document_by_id(documento_id)
    caballo = crud_caballo.get_caballo_by_id(caballo_id)
    
    client = current_app.storage.client
    client.remove_object("grupo30", documento.nombre_documento)
    
    crud_caballo.delete_document(documento.id)
    
    return render_template("caballos/show.html", caballo=caballo)

@caballos_documentos_bp.get("/documentos/descargar/<int:documento_id>")
@login_required
@check("horse_show")
def download_documento(documento_id):
    """
    Permite la descarga de un documento específico asociado a un caballo.

    Args:
        documento_id: ID del documento a descargar.

    Returns:
        Archivo descargable con los datos del documento.
    """
    documento = crud_caballo.get_document_by_id(documento_id)
    client = current_app.storage.client
    bucket_name = "grupo30"
    file_name = documento.nombre_documento

    data = client.get_object(bucket_name, file_name)
    file_data = BytesIO(data.read())
    file_data.seek(0)

    return send_file(file_data, as_attachment=True, download_name=documento.nombre_documento)