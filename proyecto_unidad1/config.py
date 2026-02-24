import os

class Config:
    SECRET_KEY = 'secret'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/app_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False