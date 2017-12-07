import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'This string will be replaced with a proper key in production.'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(BASEDIR, 'data.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN')
MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')

PROPAGATE_EXCEPTIONS = True

THREADS_PER_PAGE = 8

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = "somethingimpossibletoguess"

ADMINS = frozenset(['jslvtr@gmail.com'])
