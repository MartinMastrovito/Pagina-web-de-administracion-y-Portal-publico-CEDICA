from flask import render_template, request, Blueprint, flash, redirect
from src.core import crud_JyA
from src.core.auth.decorators import login_required, check

bp = Blueprint("enlaces", __name__, url_prefix="/JYA/documentos")

@bp.get("/cargar_enlace/<int:jya_dni>")
@login_required
@check("jya_new")
def show_upload_link(jya_dni):
    """
    Muestra el formulario para cargar un nuevo enlace asociado a un JYA.

    Args:
        jya_dni (int): DNI del JYA para el cual se carga el enlace.

    Returns:
        Renderizado de la plantilla upload_link.html.
    """
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    return render_template("JYA/upload_link.html", jya=jya)

@bp.post("/cargar_enlace/<int:jya_dni>")
@login_required
@check("jya_new")
def upload_link(jya_dni):
    """
    Carga un enlace asociado a un JYA y lo guarda en la base de datos.

    Args:
        jya_dni (int): DNI del JYA para el cual se carga el enlace.

    Returns:
        Renderizado de la plantilla show_jya.html después de cargar el enlace.
    """
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    documento = request.form["documento"]

    if not documento.startswith(("http://", "https://")):
        documento = "https://" + documento

    doc_data = {
        "nombre_documento": documento,
        "tipo_documento": request.form["tipo"],
        "jya_dni": jya_dni,
    }
    
    crud_JyA.save_document(**doc_data)
    
    flash('Se ha subido el enlace exitosamente!.', 'success')
    return redirect(f"/JYA/documentos/{jya_dni}")

@bp.get("/actualizar_link/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_update")
def show_update_link_jya(jya_dni, documento_id):
    """
    Muestra el formulario para actualizar un enlace específico de un JYA.

    Args:
        jya_dni (int): DNI del JYA al que pertenece el enlace.
        documento_id (int): ID del enlace a actualizar.

    Returns:
        Renderizado de la plantilla edit_link_jya.html.
    """
    documento = crud_JyA.get_document_by_id(documento_id)
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    return render_template("JYA/edit_link_jya.html", jya=jya, documento=documento)

@bp.post("/actualizar_link/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_update")
def update_link_jya(jya_dni, documento_id):
    """
    Actualiza un enlace de un JYA, reemplazándolo en la base de datos.

    Args:
        jya_dni (int): DNI del JYA al que pertenece el enlace.
        documento_id (int): ID del enlace a actualizar.

    Returns:
        Renderizado de la plantilla show_jya.html después de actualizar el enlace.
    """
    documento = crud_JyA.get_document_by_id(documento_id)
    
    enlace = request.form["documento"]

    if not enlace.startswith(("http://", "https://")):
        enlace = "https://" + enlace

    doc_data = {
        "nombre_documento": enlace,
        "tipo_documento": request.form["tipo"],
    }
        
    crud_JyA.update_document(documento.id, **doc_data)
    
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    flash('Se ha actualizado el enlace exitosamente!.', 'success')
    return redirect(f"/JYA/documentos/{jya_dni}")

@bp.get("/eliminar_link/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_destroy")
def show_delete_link_jya(jya_dni, documento_id):
    """
    Muestra la confirmación para eliminar un enlace específico de un JYA.

    Args:
        jya_dni (int): DNI del JYA al que pertenece el enlace.
        documento_id (int): ID del enlace a eliminar.

    Returns:
        Renderizado de la plantilla delete_link_jya.html.
    """
    documento = crud_JyA.get_document_by_id(documento_id)
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    return render_template("JYA/delete_link_jya.html", jya=jya, documento=documento)

@bp.post("/eliminar_link/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_destroy")
def delete_link_jya(jya_dni, documento_id):
    """
    Elimina un enlace de un JYA de la base de datos.

    Args:
        jya_dni (int): DNI del JYA al que pertenece el enlace.
        documento_id (int): ID del enlace a eliminar.

    Returns:
        Renderizado de la plantilla show_jya.html después de la eliminación.
    """
    documento = crud_JyA.get_document_by_id(documento_id)
    
    crud_JyA.delete_document(documento.id)

    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    flash('Se ha eliminado el enlace exitosamente!.', 'success')
    return redirect(f"/JYA/documentos/{jya_dni}")
