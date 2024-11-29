from os import fstat
from flask import render_template, request, send_file, Blueprint, current_app, redirect
from src.core import empleados
from src.core.auth.decorators import login_required, check
from io import BytesIO

bp = Blueprint("documentos_empleado", __name__, url_prefix="/documentos_empleado")

@bp.get("/<int:empleado_dni>")
@login_required
@check("team_index")
def index(empleado_dni):
    """
    Muestra la lista de documentos asociados a un empleado específico,
    con opciones de búsqueda y ordenamiento.

    Args:
        empleado_dni: DNI del empleado cuyos documentos se listan.

    Returns:
        Renderizado de la plantilla show_documents_empleado.html con los documentos y paginación.
    """
    empleado = empleados.get_empleado_por_dni(empleado_dni)
    
    nombre_documento = request.args.get("nombre_documento")
    sort_by = request.args.get("sort_by", "nombre_documento")
    order = request.args.get("order", "asc")
    page = request.args.get("page", 1, type=int)
    per_page = 10
        
    documentos_pagination = empleados.search_documents(
        empleado_dni=empleado.dni,
        nombre_documento=nombre_documento,
        sort_by=sort_by,
        order=order,
        page=page,
        per_page=per_page
    )

    for documento in documentos_pagination.items:
        documento.nombre_documento = documento.nombre_documento[documento.nombre_documento.find("=")+1:]
    
    return render_template(
        "empleados/index_documents.html",
        empleado=empleado,
        documentos=documentos_pagination.items,
        pagination=documentos_pagination
    )

@bp.get("/cargar_documentos/<int:empleado_dni>")
@login_required
@check("team_new")
def show_upload_document(empleado_dni):
    """
    Muestra el formulario para cargar un nuevo documento asociado a un empleado.

    Args:
        empleado_id: ID del empleado para el cual se carga el documento.

    Returns:
        Renderizado de la plantilla upload_document.html.
    """
    empleado = empleados.get_empleado_por_dni(empleado_dni)
    return render_template("empleados/upload_document.html", empleado=empleado)

@bp.post("/documentos/cargar_documentos/<int:empleado_dni>")
@login_required
@check("team_new")
def upload_document(empleado_dni):
    """
    Carga un documento asociado a un empleado en el almacenamiento y lo guarda en la base de datos.

    Args:
        empleado_id: ID del empleado para el cual se carga el documento.

    Returns:
        Renderizado de la plantilla show_empleado.html después de cargar el documento.
    """
    empleado = empleados.get_empleado_por_dni(empleado_dni)
    
    if "documento" in request.files:
        file = request.files["documento"]
        client = current_app.storage.client
        size = fstat(file.fileno()).st_size
        
        client.put_object(
            "grupo30",
            f"documentos-empleado/{empleado_dni}/{empleados.cant_documentos()}={file.filename}",
            file,
            size,
            content_type=file.content_type
        )
        
        doc_data = {
            "empleado_dni": empleado.dni,
            "nombre_documento": f"documentos-empleado/{empleado_dni}/{empleados.cant_documentos()}={file.filename}",
        }
        empleados.save_document(**doc_data)
        
    return redirect(f"/documentos_empleado/{empleado_dni}")

@bp.get("/documentos/eliminar/<int:empleado_id>/<int:documento_id>")
@login_required
@check("team_destroy")
def show_delete_document_empleado(empleado_id, documento_id):
    """
    Muestra la confirmación para eliminar un documento específico de un empleado.

    Args:
        empleado_id: ID del empleado al que pertenece el documento.
        documento_id: ID del documento a eliminar.

    Returns:
       Renderizado de la plantilla delete_document_empleado.html.
    """
    documento = empleados.get_document_by_id(documento_id)
    empleado = empleados.get_empleado_by_id(empleado_id)
    
    return render_template("empleados/delete_document.html", empleado=empleado, documento=documento)

@bp.post("/documentos/eliminar/<int:empleado_id>/<int:documento_id>")
@login_required
@check("team_destroy")
def delete_document_empleado(empleado_id, documento_id):
    """
    Elimina un documento de un empleado tanto del almacenamiento como de la base de datos.

    Args:
        empleado_id: ID del empleado al que pertenece el documento.
        documento_id: ID del documento a eliminar.

    Returns:
        Renderizado de la plantilla show_empleado.html después de la eliminación.
    """
    documento = empleados.get_document_by_id(documento_id)
    empleado = empleados.get_empleado_by_id(empleado_id)
    
    client = current_app.storage.client
    client.remove_object("grupo30", documento.nombre_documento)
    
    empleados.delete_document(documento.id)
    
    return redirect(f"/documentos_empleado/{empleado.dni}")

@bp.get("/documentos/descargar/<int:documento_id>")
@login_required
@check("team_show")
def download_documento(documento_id):
    """
    Permite la descarga de un documento específico asociado a un empleado.

    Args:
        documento_id: ID del documento a descargar.

    Returns:
        Archivo descargable con los datos del documento.
    """
    documento = empleados.get_document_by_id(documento_id)
    client = current_app.storage.client
    bucket_name = "grupo30"
    file_name = documento.nombre_documento

    data = client.get_object(bucket_name, file_name)
    file_data = BytesIO(data.read())
    file_data.seek(0)

    return send_file(file_data, as_attachment=True, download_name=documento.nombre_documento)
