class Config(object):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.sqlite3'
    SECRET_KEY = "thisissecret"
    SECURITY_PASSWORD_SALT = "thisissaltt"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = False
    SECURITY_TOKEN_AUTHENTICATION_HEADER = 'Authentication-Token'

class DevelopmentConfig(Config):
    DEBUG = True
    CACHE_TYPE = "RedisCache"
    CACHE_REDIS_HOST = "localhost"
    CACHE_REDIS_PORT = 6379