#!/usr/bin/python

import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True

WTF_CSRF_ENABLED = True
SECRET_KEY = '5e1441fc39978b4c93c8413bdde39170'


################################################
# Use google for email server
################################################
#MAIL_SERVER = 'smtp.googlemail.com'
#MAIL_PORT = 465
#MAIL_USE_TLS = False
#MAIL_USE_SSL = True
#MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
#MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

# administrator list
#ADMINS = ['your-gmail-username@gmail.com']

# email server
MAIL_SERVER = 'your.mailserver.com'
MAIL_PORT = 25
MAIL_USERNAME = None
MAIL_PASSWORD = None

# administrator list
ADMINS = ['you@example.com']
MAIL_SUPPRESS_SEND = True