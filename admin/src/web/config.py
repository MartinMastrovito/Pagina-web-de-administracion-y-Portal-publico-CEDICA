from os import environ
import os 
class Config(object):
    TESTING = False
    SECRET_KEY = "grupo30"

class ProductionConfig(Config):
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCESS_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,
        "pool_recycle": 60,
        "pool_pre_ping": True,
    }


""" MINIO_SERVER = "minio.proyecto2024.linti.unlp.edu.ar"
    MINIO_ACCESS_KEY = "RYZT62lu0qa8LTWqQyl3"
    MINIO_SECRET_KEY = "I94NDTB1iDXCxvifqooxFRpzEtVmQojszGv6ZNAR"
    MINIO_SECURE = False
    DB_USER = os.getenv("DB_USER", os.getlogin())  # obtener el nombre de usuario del sistema
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")  # permitir que cada usuario configure su contraseña
    ======="""

class DevelopmentConfig(Config):
    MINIO_SERVER = "localhost:9000"
    MINIO_ACCESS_KEY = "KLpAmkPAkfmLvWDtrmkt"
    MINIO_SECRET_KEY = "1Qcyj4ZrkWAqINZ54ryENCNsQx4F5QvI5zQx8GiP"
    MINIO_SECURE = False
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
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