from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from wtforms.fields import EmailField

class RegisterForm(FlaskForm):
    fullname = StringField('Full Name', validators=[
        validators.DataRequired()
    ])
    email = EmailField('Email', validators=[
        validators.DataRequired()
    ])
    username = StringField('Username', validators=[
        validators.DataRequired(),
        validators.Length(min=4, max=25)
    ])
    password = PasswordField('New Password', validators=[
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match'),
        validators.Length(min=4, max=25)
    ])
    confirm = PasswordField('Repeat Password')

    class Meta:
        csrf = False 


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
        validators.DataRequired(),
        validators.Length(min=4, max=25)
    ])
    password = PasswordField('Password', validators=[
        validators.DataRequired(),
        validators.Length(min=4, max=25)
    ])