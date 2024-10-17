# src/web/__init__.py
from flask import Flask
from flask_migrate import Migrate  # Importar Migrate
from web import routes
from core.bcrypt import bcrypt
from core.database import db_reset 
from core.database import db # Importar 'db' desde 'core.database'
from web.config import config
from web.handlers.error import not_found_error
from web.handlers.error import internal_server_error
from web.handlers.auth import check_permission

# Inicializa Migrate aquí para poder usarlo en create_app
migrate = Migrate()  

def create_app(env="development"):
    app = Flask(__name__, template_folder='../web/templates', static_folder='../../static/')

    # Clave secreta necesaria para manejar sesiones de forma segura
    app.config['SECRET_KEY'] = 'clave_secreta_super_segura'

    # Cargar la configuración del entorno
    app.config.from_object(config[env])

    #importar los modelos 
    #from src.core.auth.models.model_caballos import Caballo
    #from src.core.auth.models.model_JyA import TipoJA
    #from src.core.auth.models.model_documento import Documento
    #from src.core.auth.models.model_permission import Permission

    # Inicializar la base de datos y migraciones
    db.init_app(app)  # Inicializa SQLAlchemy con la app
    migrate.init_app(app, db)  # Inicializa Migrate con la app y db

    # Inicializar Bcrypt
    bcrypt.init_app(app)

    # Registrar rutas
    routes.register(app)

    # Manejar errores
    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_server_error)

    # Register functions on jinja
    app.jinja_env.globals.update(check_permission=check_permission)

    @app.cli.command(name="reset-db")
    def reset_db():
        """Comando para resetear la base de datos."""
        db_reset()

    return app
