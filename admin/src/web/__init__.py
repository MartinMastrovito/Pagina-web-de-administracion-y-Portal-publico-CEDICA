from flask import Flask, session
from web import routes
from core.bcrypt import bcrypt
<<<<<<< HEAD
from core import database
from src.web.storage import storage
=======
from core.database import db, db_reset # Importar 'db' desde 'core.database'
>>>>>>> 8fee9b7a120b35b621612a353d27f36a3cdd3462
from web.config import config
from web.handlers.error import not_found_error
from web.handlers.error import internal_server_error

def create_app(env="development"):
    app = Flask(__name__, template_folder='../web/templates', static_folder='../../static/')

<<<<<<< HEAD
def create_app(env = "development", static_folder = "'../../static/'"):
	app = Flask(__name__, template_folder='../web/templates',static_folder='../../static/')
        
	app.config.from_object(config[env])
	
	database.init_app(app)
	
	# Init bcrypt
	bcrypt.init_app(app)
	
	# Register routes
	routes.register(app)

	#registrar objeto storage
	storage.init_app(app)
 
	app.register_error_handler(404, not_found_error)
	app.register_error_handler(500,internal_server_error)
	
	@app.cli.command(name="reset-db")
	def reset_db():
		database.reset()
  
	return app
	
=======
    # Clave secreta necesaria para manejar sesiones de forma segura
    app.config['SECRET_KEY'] = 'clave_secreta_super_segura'

    app.config.from_object(config[env])

    # Inicializar la base de datos
    db.init_app(app)

    # Init bcrypt
    bcrypt.init_app(app)

    # Register routes
    routes.register(app)

    app.register_error_handler(404, not_found_error)
    app.register_error_handler(500, internal_server_error)

    @app.cli.command(name="reset-db")
    def reset_db():
        # Lógica para resetear la base de datos
        db_reset()

    return app
>>>>>>> 8fee9b7a120b35b621612a353d27f36a3cdd3462
