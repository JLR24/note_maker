from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import current_user, login_required

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        pass
    return render_template("login.html", user=current_user)


@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        pass
    return render_template("signup.html", user=current_user)