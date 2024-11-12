from flask import render_template, Blueprint, request, redirect, url_for, flash
from src.web.controllers.users import bp as users_bp
from src.web.controllers.invoices import invoices_bp
from src.web.controllers.gestion_jya.crud_JyA import bp as crud_JyA_bp
from src.web.controllers.gestion_jya.jya_archivos import bp as jya_archivos_bp
from src.web.controllers.gestion_jya.jya_enlaces import bp as jya_enlaces_bp
from src.web.controllers.caballos import caballos_bp
from src.web.controllers.pagos import pago_bp
from src.web.controllers.empleados import empleados_bp
from src.web.controllers.reportes import bp as reportes_bp

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
        
        return render_template('login.html')  
 
    
    # Register blueprints    
    app.register_blueprint(users_bp)

    app.register_blueprint(invoices_bp)
    
    app.register_blueprint(crud_JyA_bp)
    
    app.register_blueprint(jya_archivos_bp)
    
    app.register_blueprint(jya_enlaces_bp)

    app.register_blueprint(caballos_bp) 

    app.register_blueprint(pago_bp) 

    app.register_blueprint(empleados_bp)
    
    app.register_blueprint(reportes_bp)
