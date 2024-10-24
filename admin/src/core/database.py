from flask_sqlalchemy import SQLAlchemy

# Crear la instancia de SQLAlchemy
db = SQLAlchemy()


def init_app(app):
    """
        inicializa la base de datos con la app flask
    """
    db.init_app(app)
    config(app)


    return app


def config(app):
    """
        configuracion de hooks para la base de datos
    """
    @app.teardown_appcontext

    def close_session(exception=None):
        db.session.close()
    
    return app

def db_reset():
    """
        reseta la bd
    """
    print("eliminando la base de datos...")
    db.drop_all()
    print("creando base nueva...")
    db.create_all()
    print("listo!")