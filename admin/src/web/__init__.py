from flask import Flask
from flask import render_template
from src.web.handlers.error import not_found_error


def create_app(env = "development", static_folder = ""):
	app = Flask(__name__)
        
	@app.route("/") 
	def home():

		return render_template('home.html')

	app.register_error_handler(404, not_found_error)
	return app