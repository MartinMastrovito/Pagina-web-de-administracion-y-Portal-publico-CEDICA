from flask import Flask
from web import routes
from core.bcrypt import bcrypt
from core import database
from web.config import config
from web.handlers.error import not_found_error
from web.handlers.error import internal_server_error


def create_app(env = "development", static_folder = "'../../static/'"):
	app = Flask(__name__, template_folder='../web/templates',static_folder='../../static/')
        
	app.config.from_object(config[env])
	
	database.init_app(app)
	
	# Init bcrypt
	bcrypt.init_app(app)
	
	# Register routes
	routes.register(app)
 
	app.register_error_handler(404, not_found_error)
	app.register_error_handler(500,internal_server_error)
	
	@app.cli.command(name="reset-db")
	def reset_db():
		database.reset()
  
	return app
	
