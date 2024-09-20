import os

class Config(object):
    TESTING = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = None

class DevelopmentConfig(Config):
    DB_USER = os.getenv("DB_USER", os.getlogin())  # obtener el nombre de usuario del sistema
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")  #permitir que cada usuario configure su contraseña
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