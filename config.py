import os

from sqlalchemy import create_engine

class Config(object):
    SECRET_KEY = "Clave Secreta"
    SESSION_COOKIE_SECURE = False

class DevelopmentConfig(Config):
    Debug: True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1/examenPizza'
    SQLALCHEMY_TRACK_MODIFICATIONS = False