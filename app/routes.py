from app import db
from app import app
from app.models import User
from app.forms import RegistrationForm
from flask import render_template, flash, redirect, url_for

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