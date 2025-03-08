import sqlalchemy as sa
from flask_wtf import FlaskForm
from wtforms.validators import (
    DataRequired, 
    ValidationError, 
    Email, 
    EqualTo, 
    Length
)
from wtforms import (
    StringField, 
    PasswordField, 
    BooleanField, 
    SubmitField, 
    DateField, 
    SelectField, 
    TextAreaField,
    FileField,
    HiddenField
)

from app import db
from app.models import User, Hospital
from app.enums import GenderEnum, BloodGroupEnum
from app.validators import (
    PasswordStrength, 
    FileExtensionValidator, 
    FileMimeTypeValidator
)

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
    
    def validate_phone(self, phone):
        user = db.session.scalar(sa.select(User).where(
            User.phone == phone.data
        ))
        if user is not None:
            raise ValidationError("Please use a different phone number")

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

class ProfileForm(FlaskForm):
    avatar = FileField('Upload Avatar', validators=[
        FileExtensionValidator(allowed_extensions={'jpg', 'jpeg', 'png'}),
        FileMimeTypeValidator(allowed_mimetypes={'image/jpeg', 'image/png'})
    ])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10, max=15)])
    dob = DateField("Date of Birth", format='%Y-%m-%d', validators=[DataRequired()])
    gender = SelectField("Gender", choices=[(g.name, g.value) for g in GenderEnum], validators=[DataRequired()])
    address = TextAreaField("Address", validators=[DataRequired(), Length(min=3, max=120)])
    city_or_town = StringField("City or Town", validators=[DataRequired(), Length(min=3, max=64)])
    state = StringField("State", validators=[DataRequired(), Length(min=3, max=100)])
    zip_code = StringField("Zip Code", validators=[DataRequired(), Length(min=5, max=10)])
    blood_group = SelectField("Blood Group", choices=[(bg.name, bg.value) for bg in BloodGroupEnum])
    submit = SubmitField("Update")

class HospitalForm(FlaskForm):
    image = FileField('Upload Image', validators=[
        FileExtensionValidator(allowed_extensions={'jpg', 'jpeg', 'png'}),
        FileMimeTypeValidator(allowed_mimetypes={'image/jpeg', 'image/png'})
    ])
    name = StringField("Name", validators=[DataRequired(), Length(min=3, max=63)])
    hrn = StringField("HRN", validators=[DataRequired(), Length(max=32)])
    address = TextAreaField("Address", validators=[DataRequired(), Length(min=3, max=120)])
    city_or_town = StringField("City or Town", validators=[DataRequired(), Length(min=3, max=64)])
    state = StringField("State", validators=[DataRequired(), Length(min=3, max=64)])
    zip_code = StringField("Zip Code", validators=[DataRequired(), Length(min=5, max=10)])
    phone = StringField("Phone", validators=[DataRequired(), Length(min=10, max=15)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    current_hrn = HiddenField()
    submit = SubmitField("Update")


    def validate_hrn(self, hrn):
        if hrn.data != self.current_hrn.data:
            hospital = db.session.scalar(sa.select(Hospital).where(
                Hospital.hrn == hrn.data
            ))
            if hospital is not None:
                raise ValidationError("Please use a different registration number")