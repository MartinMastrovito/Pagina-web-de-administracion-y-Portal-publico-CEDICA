from flask import render_template
from flask import Blueprint
from src.core import board 

web_blueprint = Blueprint("issues",__name__, url_prefix="/src/web/templates")

def issues_home():
    return render_template("templates/home.html")
    
