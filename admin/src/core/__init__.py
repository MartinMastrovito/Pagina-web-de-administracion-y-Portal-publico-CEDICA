from flask import Flask
from flask import render_template
from src.web.handlers.error import not_found_error
from src.web.handlers.error import internal_server_error
from src.core import database
from src.core.config import config


def create_app(env = "development", static_folder = ""):
	app = Flask(__name__, template_folder='../web/templates')
        
	app.config.from_object(config[env])
	
	database.init_app(app)
	
	
	
	
	@app.route("/") 
	def home():
		return render_template('home.html')

	app.register_error_handler(404, not_found_error)
	app.register_error_handler(500,internal_server_error)
	
	@app.cli.command(name="reset-db")
	def reset_db():
		database.reset()
	return app
	
