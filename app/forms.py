from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    """ Register New User """

    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        "if username already exists, throw validation error"

        user = User.query.filter_by(username=username.data).first()
        # If user != none (aka if there is a user)
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        "if email already exits, throw validation error"

        email = User.query.filter_by(email=email.data).first()
        # If email != none ( aka if email already exists)
        if email:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    """ Login (with email) """ 

    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
 