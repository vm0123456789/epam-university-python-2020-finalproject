import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '-very-very-SECRET-KEY-'
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://user:password@localhost:33060/departments_app"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or '-very-very-SECRET-KEY-'
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app/tests/test.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

