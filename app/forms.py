import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length

from app import db
from app.models import User
from app.validators import PasswordStrength

class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    phone = StringField("Phone", validators=[DataRequired()])
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