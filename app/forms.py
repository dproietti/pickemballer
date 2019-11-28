from .models import Player, Pool, PoolPlayer, Team, Schedule, Pics
from flask_wtf import Form
from wtforms import StringField, BooleanField, TextField, PasswordField, RadioField, HiddenField, IntegerField, FloatField, validators
from wtforms.validators import DataRequired



class PasswordChange(Form):
    
    passwordOld = PasswordField('Old password', [
        validators.Required()
    ])
    
    passwordNew = PasswordField('New Password', [
        validators.DataRequired(),
        validators.EqualTo('passwordConfirm', message='Passwords must match')
    ])
    passwordConfirm = PasswordField('Confirm new password', [
        validators.Required()
    ])

class PasswordReset(Form):
    email = TextField('Email Address', [
        validators.Required()
    ])
    
class ResetPasswordForm(Form):
    password = PasswordField('New Password', [
        validators.Required()
    ])
    
    

class RegistrationForm(Form):
    
    firstname = TextField('firstname', [
        validators.Required()
    ])
    lastname = TextField('lastname', [
        validators.Required()
    ])
    email = TextField('Email Address', [
        validators.Required()
    ])
    password = PasswordField('New Password', [
        validators.Required()
    ])
    
class ActivateUserForm(Form):
    
    key = HiddenField('key')
    
    firstname = TextField('firstname', [
        validators.Required()
    ])
    lastname = TextField('lastname', [
        validators.Required()
    ])
    password = PasswordField('New Password', [
        validators.Required()
    ])

class LoginForm(Form):
    email = TextField('Email Address', [
        validators.Required()
    ])
    password = PasswordField('New Password', [
        validators.Required()
    ])

class PoolForm(Form):
    poolname = TextField('poolname', [validators.Length(min=4, max=50)])
    pooltype = RadioField('pooltype', choices=[('pickem','PickEm'),('pick5','Pick 5'),('survivor','Survivor')])
    
class PoolAddPlayer(Form):
    poolId = HiddenField('pool_id')
    nickName  = TextField('firstname', [
        validators.Required()
    ])
    email = TextField('Email Address', [
        validators.Required()
    ])
    
class picsForm(Form):
    tieBreaker = IntegerField('tieBreaker')
    showPicks = BooleanField('showPicks')

class AddSpread(Form):
    week = HiddenField('week')
    gameId = IntegerField('gameId')
    homeLine = FloatField('homeLine')
    overUnder = FloatField('overUnder')
