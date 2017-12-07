import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SECRET_KEY = 'This string will be replaced with a proper key in production.'
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'sqlite:///' + os.path.join(BASEDIR, 'data.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

MAILGUN_DOMAIN = 'mg.schoolofcode.me'
MAILGUN_API_KEY = 'key-1f1fb4afbcec8c5fca169a0c940767cc'

PROPAGATE_EXCEPTIONS = True

THREADS_PER_PAGE = 8

WTF_CSRF_ENABLED = True
WTF_CSRF_SECRET_KEY = "somethingimpossibletoguess"

ADMINS = frozenset(['jslvtr@gmail.com'])
