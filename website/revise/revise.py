from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import current_user, login_required
from ..models import db, Module, Point

revise = Blueprint("revise", __name__, template_folder="templates", static_folder="static")


@revise.route("/")
@login_required
def index():
    return render_template("revise.html", user=current_user)


@revise.route("/module/<int:m_id>", methods=["GET", "POST"])
@login_required
def module(m_id):
    # Display creation tree, but with all sub-points as text fields.
    # On submission, check each text field (unique ID) with answer.
    # Extension is to allow for override?
    # Store answers as dictionary and pass into template (so that the user can keep trying until correct).
        # There is no need to store this in the session, since it can be redefined whenever the user presses submit.
    # Upon completion, show number of attempts, their score each time, and the total time taken.
    module = Module.query.get(m_id)
    if not module:
        flash("Invalid details!", category="error")
        return redirect(url_for("revise.index"))
    results = dict()
    count = 0
    start = 0
    if request.method == "POST":
        start = request.form.get("start")
        results, count = checkModuleAnswers(module)
        print(len(results))
        if count == len(results):
            time = request.form.get("time")
            module.attempts += 1
            db.session.commit()
            flash(f"All correct! Completed in: {time}.", category="success")
            return redirect(url_for("revise.index"))
    return render_template("revise_module.html", module=module, user=current_user, results=results, count=count, start=start)

# Similar thing as above for headings.

# And then random points within a course and module (for blank fill).


def checkModuleAnswers(module):
    '''This function takes the module object and checks the answers of the given form submission'''
    return checkChildren(dict(), 0, module)


def checkChildren(results, count, point):
    for item in point._getChildren():
        results, count = checkChildren(results, count, item)
    if type(point) == Point and not point.isRoot:
        results[point.id] = request.form.get(f"{point.id}")
    if type(point) == Point and point.checkAnswer(request.form.get(f"{point.id}")):
        count += 1
    return (results, count)