import os

class BaseConfig(object):
    'Base config class'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    FLASK_ADMIN_SWATCH = "slate"
    

class ProductionConfig(BaseConfig):
    'Production specific config'
    DEBUG = False
    TESTING  = False
    SECRET_KEY = open('./Application/keys/app_secret_key.key').read()

class DevelopmentConfig(BaseConfig):
    'Development environment specific config'
    SECRET_KEY = "eo3ahKahquaesh9ahphooph0aish7po0oo9cooShiiZ5faeBaenei9eey1dou0heecie2hoot2pi5dohtheiYemu6Ieze0OhL5oh"
