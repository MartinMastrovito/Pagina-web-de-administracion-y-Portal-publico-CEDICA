import os
from os import environ

class Config(object):
    TESTING = False
    SECRET_KEY = "grupo30"

class ProductionConfig(Config):
    """Configuracion de produccion."""
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }

class DevelopmentConfig(Config):
    DB_USER = os.getenv("DB_USER", "tu_user_name")  # obtener el nombre de usuario del sistema
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")  # permitir que cada usuario configure su contraseña
    DB_HOST = "localhost"
    DB_PORT = "5432"
    DB_NAME = "grupo30"
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

class TestingConfig(Config):
    TESTING = True

config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig, 
}