from flask import Flask
from flask_jwt_extended import JWTManager
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_mail import Mail
from flask_bcrypt import Bcrypt
from mongoengine import connect
import settings.settings
from os import environ
from urllib.parse import urlencode

params = {'retryWrites': 'true',
          'w': 'majority',
          'ssl': 'true',
          'ssl_cert_reqs': 'CERT_NONE'
         }

EMAIL = environ['EMAIL']
PSWD_EMAIL = environ['PSWD_EMAIL']
USER = environ['USER']
PSWD = environ['PSWD']
SERVER = environ['SERVER']
DB = environ['DB']
URI = 'mongodb+srv://' + USER + ':' + PSWD + SERVER + '/' + DB + '?' + urlencode(params)

client = connect(host=URI)

app = Flask(__name__, template_folder='template')

app.config.update(dict(
    JWT_SECRET_KEY = "super-secret",
    SECRET_KEY = "ultra-secret",
    SECURITY_PASSWORD_SALT = "mega-secret",
    DEBUG = True,
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 587,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = str(EMAIL),
    MAIL_PASSWORD = str(PSWD_EMAIL)
))
mail = Mail(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
limiter = Limiter(app, key_func=get_remote_address, default_limits=["80/hour"])