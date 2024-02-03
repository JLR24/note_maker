from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import current_user, login_required

create = Blueprint("create", __name__, template_folder="templates", static_folder="static")