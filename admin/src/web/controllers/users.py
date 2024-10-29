from flask import render_template, request, redirect, session, flash, url_for
from src.core.database import db
from flask import Blueprint
from src.core.auth import utiles
from src.core.auth.decorators import login_required, check
from src.core.bcrypt import check_password_hash
from src.web.validators.jya_validations import validator_email, validator_texto

bp = Blueprint("users", __name__, url_prefix="/usuarios")

@bp.get("/login")
def show_login_form():
    """Muestra el formulario de inicio de sesión."""
    return render_template("users/login.html")


@bp.get("/principal")
def show_home():
    """Muestra la página principal después del inicio de sesión."""
    return render_template("home.html")

@bp.post("/login")
def login():
    """
    Realiza el inicio de sesión del usuario.

    Verifica el email y la contraseña del usuario. Si son correctos,
    se guarda el ID del usuario en la sesión y se redirige al índice de usuarios.

    Returns:
        Redirige a la lista de usuarios o vuelve al formulario de inicio de sesión.
    """
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

@bp.get("/logout")
def logout():
    if session.get("user"):
        del session["user"]
        session.clear()
        flash("¡La sesion se cerró!","info")
    else:
        flash("No hay una sesion activa", "error")
    return redirect(url_for("users.login"))

@bp.get("/")
@login_required
@check("user_index")
def index():
    """
    Muestra la lista de usuarios con paginación y filtrado.

    Returns:
        Renderiza la plantilla con la lista de usuarios.
    """
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
        role_id=role_id,
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
    """Muestra el formulario para crear un nuevo usuario."""
    return render_template("users/create_user.html")

@bp.post("/crear_usuario")
@login_required
@check("user_new")
def create_user():
    """
    Crea un nuevo usuario en la base de datos.

    Valida los campos de entrada y crea un nuevo usuario. Si el usuario ya existe,
    se muestra un mensaje de error.

    Returns:
        Redirige al índice de usuarios o al formulario de creación si hubo un error.
    """
    user_data = {
        "email": request.form['email'],
        "alias": request.form['alias'],
        "password": request.form['password'],
        "enabled": 'enabled' in request.form,
        "role_id": request.form['role_id']
    }
    
    if (not validator_texto(user_data["alias"]) and 
            not validator_email(user_data["email"])):
        flash('Ocurrió un error al ingresar los campos, por favor intente nuevamente', 'danger')
        return redirect("/usuarios/crear_usuario")
    
    user = utiles.create_user(**user_data)
    
    if user:
        flash('Usuario creado exitosamente', 'success')
        return redirect('/usuarios')
    else:
        flash('El usuario ya existe u ocurrió un error', 'danger')
        return redirect("/usuarios/crear_usuario")

@bp.get("/actualizar/<int:user_id>")
@login_required
@check("user_update")
def show_update_user(user_id):
    """
    Muestra el formulario para actualizar un usuario existente.

    Args:
        user_id (int): ID del usuario a actualizar.

    Returns:
        Renderiza la plantilla de actualización de usuario.
    """
    user = utiles.get_user(user_id)
    return render_template("users/update_user.html", user=user)

@bp.post("/actualizar/<int:user_id>")
@login_required
@check("user_update")
def user_update(user_id):
    """
    Actualiza los datos de un usuario existente.

    Valida los campos de entrada y actualiza el usuario. Si hay un error en la
    validación, se redirige al formulario de actualización.

    Args:
        user_id: ID del usuario a actualizar.

    Returns:
        Redirige a la plantilla de actualización o al índice de usuarios si fue exitoso.
    """
    user_data = {
        'email': request.form['email'],
        'alias': request.form['alias'],
        'enabled': 'enabled' in request.form,
        'role_id': request.form['role_id']
    }
    
    if (not validator_texto(user_data["alias"]) and 
            not validator_email(user_data["email"])):
        flash('Ocurrió un error al ingresar los campos, por favor intente nuevamente', 'danger')
        return redirect(f"/usuarios/actualizar/{user_id}")
    
    mensaje = utiles.update_user(user_id, **user_data)
    if mensaje:
        flash(mensaje, 'danger')
        return redirect(f'/usuarios/actualizar/{user_id}')
    else:
        return redirect("/usuarios")

@bp.get("/eliminar/<int:user_id>")
@login_required
@check("user_destroy")
def show_delete_user(user_id):
    """
    Muestra la confirmación de eliminación de un usuario.

    Args:
        user_id: ID del usuario a eliminar.

    Returns:
        Renderiza la plantilla de confirmación de eliminación.
    """
    user = utiles.get_user(user_id)
    return render_template("users/delete_user.html", user=user)

@bp.post("/eliminar/<int:user_id>")
@login_required
@check("user_destroy")
def user_delete(user_id):
    """
    Elimina un usuario de la base de datos.

    Args:
        user_id: ID del usuario a eliminar.

    Returns:
        Response: Redirige al índice de usuarios.
    """
    if utiles.delete_user(user_id):
        flash("Usuario eliminado exitosamente.")
    else:
        flash("No se puede eliminar a un System Admin.")
    return redirect('/usuarios')

@bp.get("/block/<int:user_id>")
@login_required
@check("user_update")
def confirm_block(user_id):
    """
    Muestra la confirmación para bloquear un usuario.

    Args:
        user_id: ID del usuario a bloquear.

    Returns:
        Renderiza la plantilla de confirmación para bloquear usuario.
    """
    user = utiles.get_user(user_id)
    return render_template("users/confirm_block.html", user=user)


@bp.post("/block/<int:user_id>")
@login_required
@check("user_update")
def block(user_id):
    """
    Bloquea a un usuario.

    Args:
        user_id: ID del usuario a bloquear.

    Returns:
        Redirige al índice de usuarios con un mensaje de éxito o error.
    """
    if utiles.block_user(user_id):
        flash("Usuario bloqueado exitosamente.")
    else:
        flash("No se puede bloquear a un System Admin.")
    return redirect(url_for("users.index"))


@bp.post("/unblock/<int:user_id>")
@login_required
@check("user_update")
def unblock(user_id):
    """
    Desbloquea a un usuario.

    Args:
        user_id: ID del usuario a desbloquear.

    Returns:
        Redirige al índice de usuarios con un mensaje de éxito o error.
    """
    if utiles.unblock_user(user_id):
        flash("Usuario desbloqueado exitosamente.")
    else:
        flash("No se puede desbloquear al usuario.")
    return redirect(url_for("users.index"))