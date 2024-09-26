from flask import render_template, request, redirect
from core.database import db
from flask import Blueprint
from core.auth import utiles

bp = Blueprint("users", __name__, url_prefix="/usuarios")

@bp.get("/")
def index():
    users = utiles.list_users()
    
    return render_template("users/list_users.html", users=users)

@bp.get("/crear_usuario")
def show_create_user_form():
    return render_template("users/create_user.html")

@bp.post("/crear_usuario")
def create_user():
    
    user_data = {
        "email": request.form['email'],
        "alias": request.form['alias'],
        "password": request.form['password'],
        "enabled": 'enabled' in request.form,
        "role_id": request.form['role_id']
    }
    
    utiles.create_user(**user_data)
    
    return redirect('/usuarios')

@bp.get("/actualizar/<int:user_id>")
def show_update_user(user_id):
    user = utiles.get_user(user_id)
    return render_template("users/update_user.html", user=user)

@bp.post("/actualizar/<int:user_id>")
def user_update(user_id):
    # Obtener datos del formulario
    user_data = {
        'email': request.form['email'],
        'alias': request.form['alias'],
        'enabled': 'enabled' in request.form,  # Checkbox handling
        'role_id': request.form['role_id']
    }
    
    utiles.update_user(user_id, **user_data)

    return redirect('/usuarios')

@bp.get("/eliminar/<int:user_id>")
def show_delete_user(user_id):
    user = utiles.get_user(user_id)
    return render_template("users/delete_user.html", user=user)

@bp.post("/eliminar/<int:user_id>")
def user_delete(user_id):
    # Obtener datos del formulario
    
    utiles.delete_user(user_id)

    return redirect('/usuarios')


