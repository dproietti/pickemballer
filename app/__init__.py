import os
from flask import Flask
from flask.ext.bcrypt import Bcrypt
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin
from config import basedir
from flask.ext.mail import Mail
from flask_wtf.csrf import CsrfProtect


app = Flask(__name__)
app.config.from_object('config')
CsrfProtect(app)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views, models

mail = Mail(app)
