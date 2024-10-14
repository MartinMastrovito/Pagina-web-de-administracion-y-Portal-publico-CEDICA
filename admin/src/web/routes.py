from flask import render_template, Blueprint, request, redirect, url_for, flash
from web.controllers.users import bp as users_bp
from web.controllers.invoices import invoices_bp
from web.controllers.caballos import caballos_bp

def register(app):
    # Crear un Blueprint para las rutas
    main = Blueprint('main', __name__)

    # Ruta para la página principal (home)
    @app.route('/')
    def home():
        return render_template('home.html')

    # Ruta para el inicio de sesión
    @main.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            email = request.form['email']
            password = request.form['password']
            
            user = login_user(email, password)
            if user:
                
                flash('Inicio de sesión exitoso.', 'success')
                return redirect(url_for('main.home'))  # Redirige a la página de inicio
            else:
                flash('Correo electrónico o contraseña incorrectos.', 'danger')
        
        return render_template('login.html')  # 
    
    # Register blueprints    
    app.register_blueprint(users_bp)

    app.register_blueprint(invoices_bp)

    app.register_blueprint(caballos_bp) 




    #de
    # f pages_list():
        
     #   pages = [
      #      {
       #         "name":"home","url":url_for("home")
        #    }
        #]
        
       # return pages

	
