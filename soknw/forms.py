import email_validator
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from soknw.models import User


class  RegistrationForm(FlaskForm):
    username = StringField('Username',
                    validators=[DataRequired(),Length(min=2,max=20)])
    name = StringField('Name',
                    validators=[DataRequired(),Length(min=2,max=200)])
    email = StringField('Email',
                    validators=[DataRequired(),Email()])
    password = PasswordField('Password',
                    validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                    validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            print('---> check username validater <---')
            raise ValidationError('This username is taken. Please choose a diffrent one.')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            print('---> check email validater <---')
            raise ValidationError('This email already exist. Please try login.')


class  LoginForm(FlaskForm):
    email = StringField('Email',
                    validators=[DataRequired(),Email()])
    password = PasswordField('Password',
                    validators=[DataRequired()])
    remember = BooleanField('Remeber Me')
    submit = SubmitField('LogIn')

class  UpdateAccountForm(FlaskForm):
    avtar = FileField('Update Profile Picture', validators= [FileAllowed(['jpg','jpeg','png','gif'])]) 
    name = StringField('Name',
                    validators=[DataRequired(),Length(min=2,max=200)])
    username = StringField('Username',
                    validators=[DataRequired(),Length(min=2,max=20)])
    email = StringField('Email',
                    validators=[DataRequired(),Email()])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username :
            user = User.query.filter_by(username=username.data).first()
            if user:
                print('---> check username validater <---')
                raise ValidationError('This username is taken. Please choose a diffrent one.')


    def validate_email(self, email):
        if email.data != current_user.email :
            user = User.query.filter_by(email=email.data).first()
            if user:
                print('---> check email validater <---')
                raise ValidationError('This email already exist. Please try login.')
