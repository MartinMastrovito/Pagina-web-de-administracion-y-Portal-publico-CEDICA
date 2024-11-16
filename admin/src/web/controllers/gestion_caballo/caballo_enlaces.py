from flask import Blueprint, render_template, request, redirect, url_for
from src.core import crud_caballos as crud_caballo 
from src.core.auth.decorators import login_required, check

bp = Blueprint("caballo_enlaces", __name__, url_prefix="/caballos/documentos")


@bp.get("/enlaces/cargar_enlaces/<int:caballo_id>")
@login_required
@check("horse_new")
def show_upload_link(caballo_id):
    """
    Muestra el formulario para cargar un nuevo enlace asociado a un caballo.

    Args:
        caballo_id: ID del caballo para el cual se carga el enlace.

    Returns:
        Renderizado de la plantilla upload_link.html.
    """
    caballo = crud_caballo.get_caballo_by_id(caballo_id)
    return render_template("caballos/upload_link.html", caballo=caballo)

@bp.post("/enlaces/cargar_enlaces/<int:caballo_id>")
@login_required
@check("horse_new")
def upload_link(caballo_id):
    """
    Carga un enlace asociado a un caballo en la base de datos.

    Args:
        caballo_id: ID del caballo para el cual se carga el enlace.

    Returns:
        Redirección a la vista de enlaces del caballo.
    """
    caballo = crud_caballo.get_caballo_by_id(caballo_id)
    
    documento = request.form["documento"]

    if not documento.startswith(("http://", "https://")):
        documento = "http://" + documento

    doc_data = {
        "nombre_documento": documento,
        "tipo_documento": request.form["tipo"],
        "caballo_id": caballo_id,
    }
    
    crud_caballo.save_document(**doc_data)
    documentos = crud_caballo.list_documents(caballo_id=caballo.id)    
    return render_template('caballos/show.html', caballo=caballo, documentos=documentos)

@bp.get("/enlaces/actualizar/<int:caballo_id>/<int:documento_id>")
@login_required
@check("horse_update")
def show_update_link_caballo(caballo_id, documento_id):
    """
    Muestra el formulario para actualizar un enlace específico de un caballo.

    Args:
        caballo_id: ID del caballo al que pertenece el enlace.
        documento_id: ID del enlace a actualizar.

    Returns:
        Renderizado de la plantilla edit_link_caballo.html.
    """
    documento = crud_caballo.get_document_by_id(documento_id)
    caballo = crud_caballo.get_caballo_by_id(caballo_id)
    return render_template("caballos/edit_link_caballo.html", caballo=caballo, documento=documento)

@bp.post("/enlaces/actualizar/<int:caballo_id>/<int:documento_id>")
@login_required
@check("horse_update")
def update_link_caballo(caballo_id, documento_id):
    """
    Actualiza un enlace de un caballo en la base de datos.

    Args:
        caballo_id: ID del caballo al que pertenece el enlace.
        documento_id: ID del enlace a actualizar.

    Returns:
        Redirección a la vista de enlaces del caballo.
    """
    documento = crud_caballo.get_document_by_id(documento_id)
   
    
    enlace = request.form["documento"]

    if not enlace.startswith(("http://", "https://")):
        enlace = "http://" + enlace

    doc_data = {
        "nombre_documento": enlace,
        "tipo_documento": request.form["tipo"],
    }
        
    crud_caballo.update_document(documento.id, **doc_data)
    
    caballo = crud_caballo.get_caballo_by_id(caballo_id)
    
    documentos = crud_caballo.list_documents(caballo_id=caballo.id)
    return render_template('caballos/show.html', caballo=caballo, documentos=documentos)
  
@bp.get("/enlaces/eliminar/<int:caballo_id>/<int:documento_id>")
@login_required
@check("horse_destroy")
def show_delete_link_caballo(caballo_id, documento_id):
    """
    Muestra la confirmación para eliminar un enlace específico de un caballo.

    Args:
        caballo_id: ID del caballo al que pertenece el enlace.
        documento_id: ID del enlace a eliminar.

    Returns:
        Renderizado de la plantilla delete_link_caballo.html.
    """
    documento = crud_caballo.get_document_by_id(documento_id)
    caballo = crud_caballo.get_caballo_by_id(caballo_id)
    
    return render_template("caballos/delete_link_caballo.html", caballo=caballo, documento=documento)

@bp.post("/enlaces/eliminar/<int:caballo_id>/<int:documento_id>")
@login_required
@check("horse_destroy")
def delete_link_caballo(caballo_id, documento_id):
    """
    Elimina un enlace de un caballo de la base de datos.

    Args:
        caballo_id: ID del caballo al que pertenece el enlace.
        documento_id: ID del enlace a eliminar.

    Returns:
        Redirección a la vista de enlaces del caballo.
    """
    documento = crud_caballo.get_document_by_id(documento_id)
    
    crud_caballo.delete_document(documento.id)

    caballo = crud_caballo.get_caballo_by_id(caballo_id)

    
    documentos = crud_caballo.list_documents(caballo_id=caballo.id)
    return render_template('caballos/show.html', caballo=caballo, documentos=documentos)