from typing import Match
from flask_wtf import FlaskForm
from wtforms import ValidationError
from wtforms.fields import IntegerField, PasswordField, SubmitField, SelectField, DateField, StringField
from wtforms.fields.html5 import DateField
from wtforms.fields.simple import FileField
from wtforms.validators import DataRequired, EqualTo, Email
from .models import User, Customer, BusinessOwner


class LoginForm(FlaskForm):

    phone_number = IntegerField(label='Registered Phone Number: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired()])
    submit_btn = SubmitField(label='Login')

class RegistrationForm(FlaskForm):

    user_role = SelectField(label='Choose your role: ', choices=[('Customer', 'Customer'), ('Business', 'Business')], validators=[DataRequired()])
    phone_number = IntegerField(label='Phone Number: ', validators=[DataRequired()])
    password = PasswordField(label='Password: ', validators=[DataRequired(), EqualTo('password_match', message='Password must match!')])
    password_match = PasswordField(label='Retype Password: ', validators=[DataRequired()])
    submit_btn = SubmitField(label='Sign Up')

    def check_phone_number(self, field):

        if User.query.filter_by(phone_number=field.data).first():
            raise ValidationError('Phone Number already registered!')

class CustomerRegistrationForm(FlaskForm):

    first_name = StringField(label='First Name: ', validators=[DataRequired()])
    last_name = StringField(label='Last Name: ', validators=[DataRequired()])
    phone_number = IntegerField(label='Phone Number: ', validators=[DataRequired()])
    email = StringField(label='Email: ')
    address1 = StringField(label='Address 1: ', validators=[DataRequired()])
    address2 = StringField(label='Address 2: ')
    city = StringField(label='City: ', validators=[DataRequired()])
    zip = IntegerField(label='Zip Code: ', validators=[DataRequired()])
    state = StringField(label='State: ', validators=[DataRequired()])
    country = StringField(label='Country: ', validators=[DataRequired()])
    sex = SelectField(label='Sex: ', choices=[('M', 'M'), ('F', 'F'), ('NA', 'Donot want to mention')], validators=[DataRequired()])
    date_of_birth = DateField(label='Date of Birth: ', validators=[DataRequired()])

    submit_btn = SubmitField(label='Submit')

    def check_email(self, field):

        if Customer.query.filter_by(email=field.data).first():
            raise ValidationError('Email already present on Database.')

class BusinessOwnerRegistrationForm(FlaskForm):

    business_name = StringField(label='Business Name: ', validators=[DataRequired()])
    business_logo = FileField(label='Business Logo: ', validators=[DataRequired()])
    phone_number = IntegerField(label='Phone Number: ', validators=[])
    address1 = StringField(label='Address 1: ', validators=[DataRequired()])
    address2 = StringField(label='Address 2: ', validators=[DataRequired()])
    city = StringField(label='City: ', validators=[DataRequired()])
    zip = IntegerField(label='Zip Code: ', validators=[DataRequired()])
    state = StringField(label='State: ', validators=[DataRequired()])
    country = StringField(label='Country: ', validators=[DataRequired()])
    business_category = SelectField(label='Business Category: ', choices=[('Grocery', 'Grocery'), ('Pharmacy', 'Pharmacy'), ('Both', 'Both')], validators=[DataRequired()])

    submit_btn = SubmitField(label='Submit')