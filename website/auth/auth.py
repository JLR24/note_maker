from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.security import check_password_hash
from ..models import db, User

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        # Query the database for a user of the matching username
        user = User.query.filter(User.username == request.form.get("username") and check_password_hash(User.password, request.form.get("password"))).first()
        if user:
            login_user(user, remember=True)
            flash(f"Welcome back, {user.username}!", category="success")
            return redirect(url_for("home.home"))
        else:
            flash("Invalid login details.", category="error")
            return redirect(url_for("auth.login"))
    return render_template("login.html", user=current_user)


@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        pass
    return render_template("signup.html", user=current_user)