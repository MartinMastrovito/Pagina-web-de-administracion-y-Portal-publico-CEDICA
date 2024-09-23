from flask import render_template, Blueprint

# Crear un Blueprint para las rutas
main = Blueprint('main', __name__)

# Ruta para la página principal (home)
@main.route('/')
def home():
    return render_template('home.html')



def pages_list():
    
    pages = [
        {
            "name":"home","url":url_for("home")
        }
    ]
    
    return pages 