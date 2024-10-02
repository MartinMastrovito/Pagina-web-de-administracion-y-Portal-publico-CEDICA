from flask import render_template, Blueprint
from web.controllers.users import bp as users_bp

def register(app):
    # Crear un Blueprint para las rutas
    main = Blueprint('main', __name__)

    # Ruta para la página principal (home)
    @app.route('/')
    def home():
        return render_template('home.html')
    
    # Register blueprints    
    app.register_blueprint(users_bp)

    #def pages_list():
        
     #   pages = [
      #      {
       #         "name":"home","url":url_for("home")
        #    }
        #]
        
       # return pages

	