from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if len(email) == 0 or len(password) == 0:
            flash("Field can not be empty", category="Validation failed")
        elif user:
            if check_password_hash(user.password, password):
                flash("Login successful", category="Validation passed")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Invalid password. Try again!",
                      category="Validation failed")
        else:
            flash("This email doesn't exist. Kindly create an account first",
                  category="Validation failed")

    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/register", methods=["GET", "POST"])
def register():
    # Differentiating b/w get and post request
    if request.method == "POST":
        email = request.form.get("email")
        name = request.form.get("name")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        user = User.query.filter_by(email=email).first()

        # Validation checks
        if len(email) == 0 or len(name) == 0 or len(password1) == 0 or len(password2) == 0:
            flash("Field can not be empty", category="Validation failed")
        elif user:
            flash("Email already exists", category="Validation failed")
        elif password1 != password2:
            flash("The passwords do not match", category="Validation failed")
        elif len(name) < 2:
            flash("Name should have more than 1 character",
                  category="Validation failed")
        elif len(email) < 4:
            flash("Enter a valid email address", category="Validation failed")
        elif len(password1) < 6:
            flash("Password must contain atleast 6 characters",
                  category="Validation failed")
        else:
            newUser = User(email=email, name=name,
                           password=generate_password_hash(password1, method="sha256"))
            db.session.add(newUser)
            db.session.commit()
            login_user(newUser, remember=True)
            flash("Account successfully created",
                  category="Validation passed")
            return redirect(url_for("views.home"))
    return render_template("register.html", user=current_user)
