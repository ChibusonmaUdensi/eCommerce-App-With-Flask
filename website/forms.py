from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField, PasswordField, EmailField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange,Email, EqualTo
from email_validator import validate_email, EmailNotValidError

class SignUpForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(min=2, message='First name must be at least 2 characters long')])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(min=2, message='Last name must be at least 2 characters long')])
    email = EmailField('Email', validators=[DataRequired(), Email(message='Invalid email address')])
    password1 = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters long')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6), EqualTo('password1', message='Passwords must match')])    
    # username = StringField('Username', validators=[DataRequired(), Length(min=2, message='Username must be at least 2 characters long')])
    submit = SubmitField('Sign Up')
    
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email(message='Invalid email address')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters long')])
    submit = SubmitField('Log In')
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters long')])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6, message='Password must be at least 6 characters long')])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), Length(min=6), EqualTo('new_password', message='Passwords must match')])
    change_password = SubmitField('Change Password')
    