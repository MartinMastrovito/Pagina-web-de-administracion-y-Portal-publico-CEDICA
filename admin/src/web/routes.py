from flask import render_template, Blueprint, request, redirect, url_for, flash
from src.web.controllers.users import bp as users_bp
from src.web.controllers.invoices import invoices_bp
from src.web.controllers.gestion_jya.crud_JyA import bp as crud_JyA_bp
from src.web.controllers.gestion_jya.jya_archivos import bp as jya_archivos_bp
from src.web.controllers.gestion_jya.jya_enlaces import bp as jya_enlaces_bp
from src.web.controllers.gestion_caballo.caballos import caballos_bp
from src.web.controllers.gestion_caballo.caballo_archivos import caballos_documentos_bp as caballo_documentos_bp
from src.web.controllers.gestion_caballo.caballo_enlaces import bp as caballo_enlaces_bp
from src.web.controllers.pagos import pagos_bp
from src.web.controllers.gestion_empleado.empleados import bp as empleados_bp
from src.web.controllers.gestion_empleado.empleado_archivos import bp as documentos_empleados_bp
from src.web.controllers.consultas import consultas_bp
from src.web.controllers.reportes import bp as reportes_bp
from src.web.controllers.publicacion import bp as publicacion_bp
from src.web.api.articles import bp as articles_api_bp
from src.web.api.consulta import consulta_api_bp
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
                return redirect(url_for('main.home'))
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

    app.register_blueprint(caballo_documentos_bp) 
    
    app.register_blueprint(caballo_enlaces_bp) 

    app.register_blueprint(pagos_bp) 

    app.register_blueprint(empleados_bp)

    app.register_blueprint(reportes_bp)

    app.register_blueprint(consultas_bp)
    
    app.register_blueprint(publicacion_bp)

    app.register_blueprint(articles_api_bp)

    app.register_blueprint(consulta_api_bp)

    app.register_blueprint(documentos_empleados_bp)

	
