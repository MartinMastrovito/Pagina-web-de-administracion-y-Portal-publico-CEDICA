from flask import Flask
from flask_cors import CORS
from flask_ckeditor import CKEditor
from src.web import routes
from src.web import helpers
from src.web.storage import storage
from src.core.bcrypt import bcrypt
from src.core.database import db_reset, init_app
from src.core.seeds import db_seeds
from src.core.database import db
from src.web.config import config
from src.web.handlers.error import not_found_error
from src.web.handlers.error import internal_server_error
from src.web.handlers.auth import check_permission, check_authenticated
from src.web.autenticacion_google import oauth

ckeditor = CKEditor()

def create_app(env="development", static_folder=''):
    app = Flask(__name__, template_folder='../web/templates', static_folder='../../static/')

    # Clave secreta necesaria para manejar sesiones de forma segura
    app.config['SECRET_KEY'] = 'clave_secreta_super_segura'

    # Cargar la configuración del entorno
    app.config.from_object(config[env])

    #Habilitar CORS
    CORS(app)
    
    # oAuth Setup
    oauth.init_app(app)
    
    # ckeditor Setup
    ckeditor.init_app(app)

    # Inicializar la base de datos y migraciones
    init_app(app)
    
    #Resetea y ejecuta el seeds en la BD 
    with app.app_context():
        db_reset()
        db_seeds()
    
    # Inicializar Bcrypt
    bcrypt.init_app(app)

    # Registrar rutas
    routes.register(app)

    # Registrar storage
    storage.init_app(app)
    
    # Manejar errores
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_server_error)

    # Register functions on jinja
    app.jinja_env.globals.update(check_permission=check_permission)
    app.jinja_env.globals.update(document_url=helpers.document_url)
    app.jinja_env.globals.update(check_authenticated=check_authenticated)
    
    @app.cli.command(name="reset-db")
    def reset_db():
        """Comando para resetear la base de datos."""
        db_reset()

    @app.cli.command(name="seeds-db")
    def seeds_db():
        """Comando para agregar datos la base de datos."""
        db_seeds()

    return app
