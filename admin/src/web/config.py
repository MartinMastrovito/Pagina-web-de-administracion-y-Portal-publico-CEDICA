import os
from os import environ

class Config(object):
    TESTING = False
    SECRET_KEY = "grupo30"

class ProductionConfig(Config):
    MINIO_SERVER = environ.get("MINIO_SERVER")
    MINIO_ACCESS_KEY = environ.get("MINIO_ACCES_KEY")
    MINIO_SECRET_KEY = environ.get("MINIO_SECRET_KEY")
    MINIO_SECURE = True
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL")

class DevelopmentConfig(Config):
    MINIO_SERVER = "localhost:9000"
    MINIO_ACCESS_KEY = "9H3ZLLlZC4qX1vbZ1MJb"
    MINIO_SECRET_KEY = "mJGy8It49ebNNu2C1PaFMe5g1s6ObJ9adpzAHsWC"
    MINIO_SECURE = False
    DB_USER = os.getenv("DB_USER", os.getlogin())
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