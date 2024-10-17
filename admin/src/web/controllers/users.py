from flask import render_template, request, redirect, session, flash, url_for
from flask import Blueprint
from core.auth import utiles
from core.auth.utiles import get_user, block_user, unblock_user
from core.auth.decorators import login_required  # Importamos el decorador
from core.auth.decorators import check  # Importamos el decorador
from core.bcrypt import check_password_hash

bp = Blueprint("users", __name__, url_prefix="/usuarios")

@bp.get("/login")
def show_login_form():
    return render_template("users/login.html")

@bp.get("/principal")
def show_home():
    return render_template("layout.html")

@bp.post("/login")
def login():
    email = request.form['email']
    password = request.form['password']
    user = utiles.get_user_by_email(email) 

    if user and check_password_hash(user.password, password): 
        session['user_id'] = user.id  # Guardamos el ID del usuario en la sesión
        flash('Inicio de sesión exitoso.', 'success')
        return redirect(url_for('users.index'))  # Redirige a la lista de usuarios
    else:
        flash('Email o contraseña incorrectos.', 'danger')
        return redirect(url_for('users.show_login_form'))

@bp.get("/")
@login_required
@check("user_index")
def index():
    email = request.args.get('email')
    enabled = request.args.get('enabled')
    role_id = request.args.get('role_id', type=int)
    sort_by = request.args.get('sort_by', 'email')
    order = request.args.get('order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = 25

    users_pagination = utiles.search_users(
        email=email,
        enabled=enabled,
        role_id=role_id,  # Cambiado aquí
        sort_by=sort_by,
        order=order,
        page=page,
        per_page=per_page
    )

    return render_template(
        "users/list_users.html",
        users=users_pagination.items,
        pagination=users_pagination
    )

@bp.get("/crear_usuario")
@login_required
@check("user_new")
def show_create_user_form():
    return render_template("users/create_user.html")

@bp.post("/crear_usuario")
@login_required
@check("user_new")
def create_user():
    user_data = {
        "email": request.form['email'],
        "alias": request.form['alias'],
        "password": request.form['password'],
        "enabled": 'enabled' in request.form,
        "role_id": request.form['role_id']
    }
    user = utiles.create_user(**user_data)
    
    if user:
        flash('Usuario creado exitosamente', 'success')
        return redirect('/usuarios')
    else:
        flash('El usuario ya existe o ocurrió un error', 'danger')
        return redirect("/usuarios/crear_usuario")


@bp.get("/actualizar/<int:user_id>")
@login_required
@check("user_update")
def show_update_user(user_id):
    user = utiles.get_user(user_id)
    return render_template("users/update_user.html", user=user)

@bp.post("/actualizar/<int:user_id>")
@login_required
@check("user_update")
def user_update(user_id):
    user_data = {
        'email': request.form['email'],
        'alias': request.form['alias'],
        'enabled': 'enabled' in request.form,
        'role_id': request.form['role_id']
    }
    utiles.update_user(user_id, **user_data)
    return redirect('/usuarios')

@bp.get("/eliminar/<int:user_id>")
@login_required
@check("user_destroy")
def show_delete_user(user_id):
    user = utiles.get_user(user_id)
    return render_template("users/delete_user.html", user=user)

@bp.post("/eliminar/<int:user_id>")
@login_required
@check("user_destroy")
def user_delete(user_id):
    utiles.delete_user(user_id)
    return redirect('/usuarios')

@bp.get("/block/<int:user_id>")
@login_required
@check("user_update")
def confirm_block(user_id):
    user = get_user(user_id)
    return render_template("users/confirm_block.html", user=user)

@bp.post("/block/<int:user_id>")
@login_required
@check("user_update")
def block(user_id):
    if block_user(user_id):
        flash("Usuario bloqueado exitosamente.")
    else:
        flash("No se puede bloquear el usuario.")
    return redirect(url_for("users.index"))

@bp.post("/unblock/<int:user_id>")
@login_required
@check("user_update")
def unblock(user_id):
    print("TEASTEANDO")
    if unblock_user(user_id):
        flash("Usuario desbloqueado exitosamente.")
    else:
        flash("No se puede desbloquear el usuario.")
    return redirect(url_for("users.index"))