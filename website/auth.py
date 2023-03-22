from flask import Blueprint, render_template, redirect, request, url_for, flash
from . import db, bcrypt
from .models import User
from .forms import RegistrationForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user

auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("views.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_pw
        )
        db.session.add(user)
        db.session.commit()
        flash("Registration was successful", "success")
        return redirect(url_for("views.index"))
    return render_template("register.html", title="Sign Up", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember_me.data)
                next_page = request.args.get("next")
                return (
                    redirect(next_page)
                    if next_page
                    else redirect(url_for("views.index"))
                )
            else:
                flash("Incorrect password", "danger")
        else:
            flash("Incorrect e-email", "danger")
    return render_template("login.html", title="Login", form=form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You've been logged out.", "success")
    return redirect(url_for("views.index"))
