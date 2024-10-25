from flask import render_template, request, Blueprint
from src.core import crud_JyA
from src.core.auth.decorators import login_required, check

bp = Blueprint("enlaces", __name__, url_prefix="/JYA/documentos")

@bp.get("documentos/cargar_enlace/<int:jya_dni>")
@login_required
@check("jya_new")
def show_upload_link(jya_dni):
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    return render_template("JYA/upload_link.html", jya=jya)

@bp.post("documentos/cargar_enlace/<int:jya_dni>")
@login_required
@check("jya_new")
def upload_link(jya_dni):
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    documento = request.form["documento"]

    if not documento.startswith(("http://", "https://")):
        documento = "http://" + documento

    doc_data = {
        "nombre_documento": documento,
        "tipo_documento": request.form["tipo"],
        "jya_dni": jya_dni,
    }
    
    crud_JyA.save_document(**doc_data)
        
    return render_template("JYA/show_jya.html", jya=jya)

@bp.get("/documentos/actualizar_link/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_update")
def show_update_link_jya(jya_dni, documento_id):
    documento = crud_JyA.get_document_by_id(documento_id)
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    return render_template("JYA/edit_link_jya.html", jya=jya, documento=documento)

@bp.post("/documentos/actualizar_link/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_update")
def update_link_jya(jya_dni, documento_id):
    documento = crud_JyA.get_document_by_id(documento_id)
    
    enlace = request.form["documento"]

    if not enlace.startswith(("http://", "https://")):
        enlace = "http://" + enlace

    doc_data = {
            "nombre_documento": enlace,
            "tipo_documento": request.form["tipo"],
    }
        
    crud_JyA.update_document(documento.id, **doc_data)
    
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    return render_template("JYA/show_jya.html", jya=jya)

@bp.get("/documentos/eliminar_link/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_destroy")
def show_delete_link_jya(jya_dni, documento_id):
    documento = crud_JyA.get_document_by_id(documento_id)
    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    return render_template("JYA/delete_link_jya.html", jya=jya, documento=documento)

@bp.post("/documentos/eliminar_link/<int:jya_dni>/<int:documento_id>")
@login_required
@check("jya_destroy")
def delete_link_jya(jya_dni, documento_id):
    documento = crud_JyA.get_document_by_id(documento_id)
    
    crud_JyA.delete_document(documento.id)

    jya = crud_JyA.get_jya_by_dni(jya_dni)
    
    return render_template("JYA/show_jya.html", jya=jya)