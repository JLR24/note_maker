from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import current_user, login_required

revise = Blueprint("revise", __name__, template_folder="templates", static_folder="static")


@revise.route("/")
@login_required
def index():
    return render_template("revise.html", user=current_user)


@revise.route("/set")
@login_required
def set():
    # Pass in course ID as argument
    return "WIP"