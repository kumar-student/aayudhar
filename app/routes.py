import os
import sqlalchemy as sa
from flask import request
from urllib.parse import urlsplit
from werkzeug.utils import secure_filename
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from app import db
from app import app
from app.models import (
    User, 
    Profile, 
    Hospital
)
from app.forms import (
    RegistrationForm, 
    LoginForm, 
    ProfileForm, 
    HospitalForm
)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", title="Home")

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, phone=form.phone.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data)
        )
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

@app.route("/user/<username>")
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    return render_template("user.html", user=user)

@app.route("/user/<username>/edit", methods=["GET", "POST"])
@login_required
def profile(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))

    if current_user.is_anonymous or user != current_user and not current_user.is_admin:
        flash('You do not have permission to edit this profile.', 'danger')
        return redirect(url_for('index'))

    form = ProfileForm()

    if request.method == "GET":
        form.phone.data = user.phone
        if user.profile:
            form.dob.data = user.profile.dob
            form.gender.data = user.profile.gender.name if user.profile.gender else None
            form.address.data = user.profile.address
            form.state.data = user.profile.state
            form.zip_code.data = user.profile.zip_code
            form.blood_group.data = user.profile.blood_group.name if user.profile.blood_group else None

    if form.validate_on_submit():
        if form.avatar.data:
            file = form.avatar.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['AVATAR_UPLOAD_FOLDER'], filename))
            
            user.avatar = os.path.join('images', 'avatars', filename)
        user.phone = form.phone.data
        
        if user.profile:
            user.profile.dob = form.dob.data
            user.profile.gender = form.gender.data
            user.profile.address = form.address.data
            user.profile.state = form.state.data
            user.profile.zip_code = form.zip_code.data
            user.profile.blood_group = form.blood_group.data
        else:
            new_profile = Profile(
                dob=form.dob.data,
                gender=form.gender.data,
                address=form.address.data,
                state=form.state.data,
                zip_code=form.zip_code.data,
                blood_group=form.blood_group.data,
                user=user
            )
            db.session.add(new_profile)

        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user', username=user.username))

    return render_template('profile.html', form=form, user=user)

@app.route("/hospitals", methods=["GET", "POST"])
@login_required
def hospitals():
    hospitals = db.session.scalars(db.select(Hospital)).all()
    return render_template("hospitals.html", hospitals=hospitals)

@app.route("/hospitals/add", methods=["GET", "POST"])
@login_required
def create_hospital():
    if current_user.is_anonymous or not current_user.is_admin:
        flash('You do not have permission to create hospital record', 'danger')
        return redirect(url_for('index'))
    
    form = HospitalForm()
    if form.validate_on_submit():
        hospital = Hospital(
            name=form.name.data,
            hrn=form.hrn.data,
            address=form.address.data,
            city_or_town=form.city_or_town.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            phone=form.phone.data,
            email=form.email.data
        )
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], filename))
            
            hospital.image = os.path.join('images', 'hospitals', filename)
        db.session.add(hospital)
        db.session.commit()
        flash('Hospital added successfully', 'success')
        return redirect(url_for('hospital_details', hrn=hospital.hrn))
    else:
        print(form.errors)
    return render_template("hospital_form.html", form=form, hospital=None)

@app.route("/hospitals/<hrn>/edit", methods=["GET", "POST"])
@login_required
def edit_hospital(hrn):
    hospital = db.first_or_404(sa.select(Hospital).where(Hospital.hrn == hrn))

    if not current_user.is_admin:
        flash('You do not have permission to edit this profile.', 'danger')
        return redirect(url_for('hospitals'))
    
    form = HospitalForm()

    if request.method == "GET":
        form.name.data = hospital.name
        form.hrn.data = hospital.hrn
        form.current_hrn.data = hospital.hrn
        form.address.data = hospital.address
        form.city_or_town.data = hospital.city_or_town
        form.state.data = hospital.state
        form.zip_code.data = hospital.zip_code
        form.phone.data = hospital.phone
        form.email.data = hospital.email        

    if form.validate_on_submit():
        hospital.name = form.name.data
        hospital.hrn = form.hrn.data
        hospital.address = form.address.data
        hospital.city_or_town = form.city_or_town.data
        hospital.state = form.state.data
        hospital.zip_code = form.zip_code.data
        hospital.phone = form.phone.data
        hospital.email = form.email.data

        # Only update the image if a new one is uploaded
        if form.image.data:
            file = form.image.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['IMAGE_UPLOAD_FOLDER'], filename))
            hospital.image = os.path.join('images', 'hospitals', filename)

        db.session.commit()
        flash('Hospital details have been updated!', 'success')
        return redirect(url_for('hospital_details', hrn=hospital.hrn))
    
    return render_template("hospital_form.html", form=form, hospital=hospital)

@app.route("/hospitals/<hrn>/")
@login_required
def hospital_details(hrn):
    hospital = db.first_or_404(sa.select(Hospital).where(Hospital.hrn == hrn))
    return render_template("hospital.html", hospital=hospital)