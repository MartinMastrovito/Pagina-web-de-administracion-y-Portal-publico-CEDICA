from os import fstat
from flask import render_template, request, send_file, Blueprint, current_app
from src.core import crud_empleados as crud_empleado
from src.core.auth.decorators import login_required, check
from io import BytesIO

empleados_documentos_bp = Blueprint("empleados_documentos", __name__, url_prefix="/empleados/documentos")

# Mostrar lista de documentos asociados a un empleado
@empleados_documentos_bp.get("/<int:empleado_id>")
@login_required
@check("empleado_index")
def index_documents_empleado(empleado_id):
    """
    Muestra la lista de documentos asociados a un empleado específico,
    con opciones de búsqueda y ordenamiento.

    Args:
        empleado_id: ID del empleado cuyos documentos se listan.

    Returns:
        Renderizado de la plantilla show_documents_empleado.html con los documentos y paginación.
    """
    empleado = crud_empleado.get_empleado_by_id(empleado_id)
    nombre_documento = request.args.get("nombre_documento")
    tipo_documento = request.args.get("tipo_documento")
    sort_by = request.args.get("sort_by", "nombre_documento")
    order = request.args.get("order", "asc")
    page = request.args.get("page", 1, type=int)
    per_page = 10

    documentos_pagination = crud_empleado.list_documents(
        empleado_id=empleado_id,
        nombre_documento=nombre_documento,
        tipo_documento=tipo_documento,
        sort_by=sort_by,
        order=order,
        page=page,
        per_page=per_page
    )

    return render_template(
        "empleados/show_documents_empleado.html",
        empleado=empleado,
        documentos=documentos_pagination.items,
        pagination=documentos_pagination
    )

# Mostrar formulario para cargar documento de un empleado
@empleados_documentos_bp.get("/documentos/cargar_documentos/<int:empleado_id>")
@login_required
@check("empleado_new")
def show_upload_document(empleado_id):
    """
    Muestra el formulario para cargar un nuevo documento asociado a un empleado.

    Args:
        empleado_id: ID del empleado para el cual se carga el documento.

    Returns:
        Renderizado de la plantilla upload_document.html.
    """
    empleado = crud_empleado.get_empleado_by_id(empleado_id)
    return render_template("empleados/upload_document.html", empleado=empleado)

# Cargar documento de un empleado
@empleados_documentos_bp.post("/documentos/cargar_documentos/<int:empleado_id>")
@login_required
@check("empleado_new")
def upload_document(empleado_id):
    """
    Carga un documento asociado a un empleado en el almacenamiento y lo guarda en la base de datos.

    Args:
        empleado_id: ID del empleado para el cual se carga el documento.

    Returns:
        Renderizado de la plantilla show_empleado.html después de cargar el documento.
    """
    empleado = crud_empleado.get_empleado_by_id(empleado_id)
    
    if "documento" in request.files:
        file = request.files["documento"]
        client = current_app.storage.client
        size = fstat(file.fileno()).st_size
        
        client.put_object(
            "grupo30",
            f"documentos-empleado/{file.filename}",
            file,
            size,
            content_type=file.content_type
        )
        
        doc_data = {
            "empleado_id": empleado_id,
            "nombre_documento": f"documentos-empleado/{file.filename}",
            "tipo_documento": request.form["tipo"]
        }
        crud_empleado.save_document(**doc_data)
        
    return render_template("empleados/show_empleado.html", empleado=empleado)

# Mostrar formulario para actualizar un documento de empleado
@empleados_documentos_bp.get("/documentos/actualizar/<int:empleado_id>/<int:documento_id>")
@login_required
@check("empleado_update")
def show_update_document_empleado(empleado_id, documento_id):
    """
    Muestra el formulario para actualizar un documento específico de un empleado.

    Args:
        empleado_id: ID del empleado al que pertenece el documento.
        documento_id: ID del documento a actualizar.

    Returns:
        Renderizado de la plantilla edit_document_empleado.html.
    """
    documento = crud_empleado.get_document_by_id(documento_id)
    empleado = crud_empleado.get_empleado_by_document(documento)
    
    return render_template("empleados/edit_document_empleado.html", empleado=empleado, documento=documento)

# Actualizar un documento de un empleado
@empleados_documentos_bp.post("/documentos/actualizar/<int:empleado_id>/<int:documento_id>")
@login_required
@check("empleado_update")
def update_document_empleado(empleado_id, documento_id):
    """
    Actualiza un documento de un empleado, reemplazándolo en el almacenamiento
    y actualizando la base de datos.

    Args:
        empleado_id: ID del empleado al que pertenece el documento.
        documento_id: ID del documento a actualizar.

    Returns:
        Renderizado de la plantilla show_empleado.html después de actualizar el documento.
    """
    documento = crud_empleado.get_document_by_id(documento_id)
    
    if "documento" in request.files:
        client = current_app.storage.client
        client.remove_object("grupo30", documento.nombre_documento)
        
        file = request.files["documento"]
        size = fstat(file.fileno()).st_size
        
        client.put_object(
            "grupo30",
            f"documentos-empleado/{file.filename}",
            file,
            size,
            content_type=file.content_type
        )
        
        doc_data = {
            "nombre_documento": f"documentos-empleado/{file.filename}",
            "tipo_documento": request.form["tipo"]
        }
        crud_empleado.update_document(documento.id, **doc_data)
    
    empleado = crud_empleado.get_empleado_by_id(empleado_id)
    
    return render_template("empleados/show_empleado.html", empleado=empleado)

# Confirmar eliminación de un documento de empleado
@empleados_documentos_bp.get("/documentos/eliminar/<int:empleado_id>/<int:documento_id>")
@login_required
@check("empleado_destroy")
def show_delete_document_empleado(empleado_id, documento_id):
    """
    Muestra la confirmación para eliminar un documento específico de un empleado.

    Args:
        empleado_id: ID del empleado al que pertenece el documento.
        documento_id: ID del documento a eliminar.

    Returns:
       Renderizado de la plantilla delete_document_empleado.html.
    """
    documento = crud_empleado.get_document_by_id(documento_id)
    empleado = crud_empleado.get_empleado_by_id(empleado_id)
    
    return render_template("empleados/delete_document_empleado.html", empleado=empleado, documento=documento)

# Eliminar un documento de un empleado
@empleados_documentos_bp.post("/documentos/eliminar/<int:empleado_id>/<int:documento_id>")
@login_required
@check("empleado_destroy")
def delete_document_empleado(empleado_id, documento_id):
    """
    Elimina un documento de un empleado tanto del almacenamiento como de la base de datos.

    Args:
        empleado_id: ID del empleado al que pertenece el documento.
        documento_id: ID del documento a eliminar.

    Returns:
        Renderizado de la plantilla show_empleado.html después de la eliminación.
    """
    documento = crud_empleado.get_document_by_id(documento_id)
    empleado = crud_empleado.get_empleado_by_id(empleado_id)
    
    client = current_app.storage.client
    client.remove_object("grupo30", documento.nombre_documento)
    
    crud_empleado.delete_document(documento.id)
    
    return render_template("empleados/show_empleado.html", empleado=empleado)

# Descargar un documento de un empleado
@empleados_documentos_bp.get("/documentos/descargar/<int:documento_id>")
@login_required
@check("empleado_show")
def download_documento(documento_id):
    """
    Permite la descarga de un documento específico asociado a un empleado.

    Args:
        documento_id: ID del documento a descargar.

    Returns:
        Archivo descargable con los datos del documento.
    """
    documento = crud_empleado.get_document_by_id(documento_id)
    client = current_app.storage.client
    bucket_name = "grupo30"
    file_name = documento.nombre_documento

    data = client.get_object(bucket_name, file_name)
    file_data = BytesIO(data.read())
    file_data.seek(0)

    return send_file(file_data, as_attachment=True, download_name=documento.nombre_documento)
