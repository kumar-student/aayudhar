import os
import sqlalchemy as sa
from flask import request
from urllib.parse import urlsplit
from werkzeug.utils import secure_filename
from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required

from app import db
from app import app
from app.models import User, Profile
from app.forms import RegistrationForm, LoginForm, ProfileForm

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
        if form.avatar.data:  # This should be a file object
            file = form.avatar.data  # This is the file object
            filename = secure_filename(file.filename)  # Get the filename
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))  # Save the file
            
            # Update the user's avatar URL in the database
            current_user.avatar = os.path.join('images', 'avatars', filename)
        user.phone = form.phone.data
        
        # Update profile details
        if user.profile:
            user.profile.dob = form.dob.data
            user.profile.gender = form.gender.data
            user.profile.address = form.address.data
            user.profile.state = form.state.data
            user.profile.zip_code = form.zip_code.data
            user.profile.blood_group = form.blood_group.data
        else:
            # Create a new profile if it doesn't exist
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