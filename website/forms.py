from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, length, NumberRange


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(), length(min=2)])
    password1 = PasswordField('Enter your pasword', validators=[DataRequired(), length(min=6)])
    password2 = PasswordField('Enter your pasword', validators=[DataRequired(), length(min=6)])
    submit = SubmitField('Sign up')
    
class LoginForm(FlaskForm):
    email = EmailField('Email', validators =[DataRequired()])   
    password = PasswordField('Enter your password', validators =[DataRequired()])
    submit = SubmitField('Log in')