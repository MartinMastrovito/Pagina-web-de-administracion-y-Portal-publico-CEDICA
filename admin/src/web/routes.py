from flask import render_template, Blueprint, request, redirect, url_for, flash
from src.web.controllers.users import bp as users_bp
from src.web.controllers.invoices import invoices_bp
from src.web.controllers.crud_JyA import bp as crud_JyA_bp
from src.web.controllers.caballos import caballos_bp
from src.web.controllers.pagos import pago_bp
from src.web.controllers.empleados import empleados_bp

def register(app):
    # Crear un Blueprint para las rutas
    main = Blueprint('main', __name__)

    # Ruta para la página principal (home)
    @app.route('/')
    def home():
        return render_template('home.html')


    # Register blueprints    
    app.register_blueprint(users_bp)

    app.register_blueprint(invoices_bp)
    
    app.register_blueprint(crud_JyA_bp)

    app.register_blueprint(caballos_bp) 

    app.register_blueprint(pago_bp) 

    app.register_blueprint(empleados_bp)


    #de
    # f pages_list():
        
     #   pages = [
      #      {
       #         "name":"home","url":url_for("home")
        #    }
        #]
        
       # return pages

	

	
