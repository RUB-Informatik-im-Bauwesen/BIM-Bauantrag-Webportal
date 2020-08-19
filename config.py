import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    DATABASE_NAME = 'default_db'
    SQLALCHEMY_DATABASE_URI ='sqlite:///' + os.path.join(basedir, DATABASE_NAME + '.sqlite')
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, DATABASE_NAME + '_migrate_repo')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    DEBUG = True

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    MAIL_SERVER = 'mail.rub.de'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''

    DATABASE_HOST = '192.168.238.4'
    DATABASE_NAME = 'webportal_test'
    DATABASE_USER = 'webportal_test'
    DATABASE_PASSWORD = ''

    REST_SERVICE_URL = "http://localhost:8080/bimbau-rest/rest"

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + DATABASE_USER + ':' + DATABASE_PASSWORD + '@' + DATABASE_HOST + '/' + DATABASE_NAME
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, DATABASE_NAME + '_migrate_repo')


config = {
    'default': Config,
    'development': Development
}
