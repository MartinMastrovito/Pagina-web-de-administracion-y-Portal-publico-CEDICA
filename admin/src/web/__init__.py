from flask import Flask, session
from src.web import routes
from src.core.bcrypt import bcrypt
from src.core import database
from src.web.storage import storage
from src.web.config import config
from src.web.handlers.error import not_found_error
from src.web.handlers.error import internal_server_error

#def create_app(env="development"):
 #   app = Flask(__name__, template_folder='../web/templates', static_folder='../../static/')

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
		return database.db_reset()
  
	return app
	
