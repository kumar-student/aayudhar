import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from wtforms import (
    StringField, 
    PasswordField, 
    BooleanField, 
    SubmitField, 
    DateField, 
    SelectField, 
    TextAreaField,
    FileField
)

from app import db
from app.models import User
from app.validators import PasswordStrength
from app.enums import GenderEnum, BloodGroupEnum

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10, max=15)])
    password = PasswordField("Password", validators=[DataRequired(), PasswordStrength()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(
            User.username == username.data
        ))
        if user is not None:
            raise ValidationError("Please use a different username")
        
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data
        ))
        if user is not None:
            raise ValidationError("Please use a different email address")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class ProfileForm(FlaskForm):
    avatar = FileField('Upload Avatar')
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10, max=15)])
    dob = DateField("Date of Birth", format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField("Gender", choices=[(g.name, g.value) for g in GenderEnum], validators=[DataRequired()])
    address = TextAreaField("Address", validators=[DataRequired(), Length(min=3, max=120)])
    state = StringField("State", validators=[DataRequired(), Length(min=3, max=100)])
    zip_code = StringField("Zip Code", validators=[DataRequired(), Length(min=5, max=10)])
    blood_group = SelectField("Blood Group", choices=[(bg.name, bg.value) for bg in BloodGroupEnum])
    submit = SubmitField("Update")