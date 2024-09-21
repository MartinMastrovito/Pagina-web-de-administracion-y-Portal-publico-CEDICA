from flask import Flask
from flask import render_template
from src.web.handlers.error import not_found_error
from src.core import database
from src.core.config import config
from src.web.controllers.issues import web_blueprint

def create_app(env = "development", static_folder = ""):
	app = Flask(__name__)
        
	app.config.from_object(config[env])
	
	database.init_app(app)
	
	app.register_blueprint(web_blueprint)
	app.register_error_handler(404, not_found_error)
	
	@app.cli.command(name="reset-db")
	def reset_db():
		database.reset()
	return app
	
