from flask import Blueprint, render_template
from flask_login import current_user

home = Blueprint("home", __name__, template_folder="templates", static_folder="home_static")

@home.route("/")
def index():
    '''Displays the home page, which contains an "about the site" section (with examples), as well as appropriate links to log in or sign up.'''
    return render_template("home.html", user=current_user)


@home.route("/privacy")
def privacy():
    '''Displays some information about privacy. This does not actually apply, since the site is not currently intended for public use.'''
    return render_template("privacy.html", user=current_user)


@home.route("/contact")
def contact():
    '''Displays contact information (hours, email, etc).'''
    return render_template("contact.html", user=current_user)