from flask import render_template, request, redirect, session, flash, url_for
from flask import Blueprint
from src.core.auth import utiles
from src.core.auth.decorators import login_required, check
from src.core.bcrypt import check_password_hash
from src.web.validators.jya_validations import validator_email, validator_texto
from src.web.autenticacion_google import oauth

bp = Blueprint("users", __name__, url_prefix="/usuarios")
    
google = oauth.register(
        name='google',
        client_id="41501282078-0df5crdiivgj0a5no3ke67rhf718t1rb.apps.googleusercontent.com",
        client_secret="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",
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
        client_kwargs={'scope': 'email profile'},
        server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
    )    
    
@bp.route('/login_google')
def login_google():
    google = oauth.create_client('google')
    redirect_uri = url_for('users.authorize', _external=True)
    return google.authorize_redirect(redirect_uri)


@bp.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()
    
    existing_user = utiles.get_user_by_email(user_info['email'])
    
    if not existing_user:
        given_name = user_info['given_name'].strip().replace(" ", "")
        alias = f"{given_name}"
        utiles.create_google_user(user_info['email'], alias)
        flash('Se ha registrado su solicitud. Espere la aprobacion de un System Admin.', 'success')
        session['profile'] = user_info
        session.permanent = True
    else:
        session['user_id'] = existing_user.id
        session['email'] = existing_user.email
        session['profile'] = user_info
        session.permanent = True
        if existing_user.enabled:
            flash('Inicio de sesión exitoso.', 'success')
        elif not existing_user.role_id:
            flash("Aun no ha sido aprobado por un System Admin. Vuelve a intentarlo más tarde.", "danger")
        else:
            flash('Esta cuenta se encuentra bloqueada del sistema.', 'danger')
    return redirect('/')

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

    if user and user.enabled and check_password_hash(user.password, password): 
        session['user_id'] = user.id
        flash('Inicio de sesión exitoso.', 'success')
        return redirect(url_for('users.show_home'))
    else:
        if user and not user.enabled:
            flash('Esta cuenta se encuentra bloqueada del sistema.', 'danger')
        else:
            flash('Email o contraseña incorrectos.', 'danger')
        return redirect(url_for('users.show_login_form'))

@bp.get("/logout")
def logout():
    if session.get("user_id"):
        del session["user_id"]
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
    per_page = 10

    unaccepted_users = utiles.unaccepted_users()

    if unaccepted_users > 0:
        flash(f"Hay {unaccepted_users} usuario(s) pendiente(s) de aceptación.", "info")

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
        pagination=users_pagination,
        unaccepted_users=unaccepted_users,
    )


@bp.get("/unaccepted")
@login_required
@check("user_accept")
def index_unaccepted():
    """
    Muestra la lista de usuarios no aceptados con paginación y filtrado.

    Returns:
        Renderiza la plantilla con la lista de usuarios no aceptados.
    """
    email = request.args.get('email')
    order = request.args.get('order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    users_pagination = utiles.search_unaccepted_users(
        email=email,
        order=order,
        page=page,
        per_page=per_page
    )

    return render_template(
        "users/list_unaccepted_users.html",
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
        flash('El email ingresado ya está siendo usado, por favor ingrese uno distinto', 'danger')
        return redirect("/usuarios/crear_usuario")

@bp.get("/accept/<int:user_id>")
@login_required
@check("user_accept")
def show_user_accept(user_id):
    """
    Muestra el formulario para aceptar a un usuario.

    Args:
        user_id (int): ID del usuario a aceptar.

    Returns:
        Renderiza la plantilla de la aceptacion de usuario.
    """
    user = utiles.get_user(user_id)
    return render_template("users/accept_user.html", user=user)

@bp.post("/accept/<int:user_id>")
@login_required
@check("user_accept")
def user_accept(user_id):
    role_id = request.form['role_id']
    utiles.accept_user(user_id, role_id)
    flash('Usuario aceptado exitosamente', 'success')
    return redirect("/usuarios/unaccepted")
    
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
        'role_id': request.form['role_id']
    }
    
    if not validator_texto(user_data["alias"]):
        flash('Ocurrió un error al ingresar el alias, por favor intente nuevamente.', 'danger')
        return redirect(f"/usuarios/actualizar/{user_id}")
    if not validator_email(user_data["email"]):
        flash('Ocurrió un error al ingresar el email, por favor intente nuevamente.', 'danger')
        return redirect(f"/usuarios/actualizar/{user_id}")
    
    mensaje = utiles.update_user(user_id, **user_data)
    if mensaje:
        flash(mensaje, 'danger')
        return redirect(f'/usuarios/actualizar/{user_id}')
    else:
        flash('Usuario actualizado correctamente', 'success')
        return redirect("/usuarios")

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
        flash("Usuario eliminado del sistema exitosamente.")
    else:
        flash("No se puede eliminar a un System Admin.")
    return redirect('/usuarios')

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
    return redirect("/usuarios")


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