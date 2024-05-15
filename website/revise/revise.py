from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import current_user, login_required
from ..models import db, Module, Point, Heading

revise = Blueprint("revise", __name__, template_folder="templates", static_folder="static")


@revise.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        m_code = request.form.get("code")
        if request.form.get("headings:" + m_code) == "All":
            return redirect(url_for("revise.module", m_code=m_code))
        return redirect(url_for("revise.heading", h_id=request.form.get("headings:" + m_code)))
    return render_template("revise.html", user=current_user)


@revise.route("/module/<string:m_code>", methods=["GET", "POST"])
@login_required
def module(m_code):
    # Display creation tree, but with all sub-points as text fields.
    # On submission, check each text field (unique ID) with answer.
    # Extension is to allow for override?
    # Store answers as dictionary and pass into template (so that the user can keep trying until correct).
        # There is no need to store this in the session, since it can be redefined whenever the user presses submit.
    # Upon completion, show number of attempts, their score each time, and the total time taken.
    module = Module.query.filter_by(code=m_code).first()
    if not module:
        flash("Invalid details!", category="error")
        return redirect(url_for("revise.index"))
    results = dict()
    count = 0
    start = 0
    if request.method == "POST":
        start = request.form.get("start")
        results, count = checkModuleAnswers(module)
        if count == len(results):
            time = request.form.get("time")
            module.attempts += 1
            # if not module.time or module.time < time:
            if not module.time or isBetterTime(module, time):
                module.time = time
            db.session.commit()
            flash(f"All correct! Completed in: {time}.", category="success")
            return redirect(url_for("revise.index"))
    return render_template("revise_module.html", module=module, user=current_user, results=results, count=count, start=start)

# Similar thing as above for headings.

@revise.route("/heading/<int:h_id>", methods=["GET", "POST"])
@login_required
def heading(h_id):
    print("RUNNING")
    h = Heading.query.filter_by(id=h_id).first()
    if not h:
        flash("Invalid details!", category="error")
        return redirect(url_for("revise.index"))
    results = dict()
    count = 0
    start = 0
    if request.method == "POST":
        start = request.form.get("start")
        results, count = checkModuleAnswers(h)
        if count == len(results):
            time = request.form.get("time")
            h.attempts += 1
            if not h.time or isBetterTime(h, time):
                h.time = time
            db.session.commit()
            flash(f"All correct! Completed in: {time}.", category="success")
            return redirect(url_for("revise.index"))
    return render_template("revise_heading.html", heading=h, user=current_user, results=results, count=count, start=start)

# And then random points within a course and module (for blank fill).

def isBetterTime(module, js_time):
    '''Returns True if the js_time is shorter than the module's time. False otherwise.'''
    try:
        module_int = getTimeStringAsInt(module.time)
        js_int = getTimeStringAsInt(js_time)

        if module_int >= js_int:
            return True
        return False
    except:
        print("Error in <revise.isBetterTime()>: module: " + module.id + "(" + module.time + ") jsTime: " + js_time)
        return False
    
def getTimeStringAsInt(time_string):
    '''Takes a string of the form 'y minute(s), z second(s)' or 'x hour(s), y minute(s), z second(s)' and returns (y * 60 + z) or (x * 3600 + y * 60 + z) respectively.'''
    try:
        time_array = time_string.split(" ")
        if (len(time_array) == 2):
            return int(time_array[0])
        elif len(time_array) == 4:
            return int(time_array[0]) * 60 + int(time_array[2])
        else:
            return int(time_array[0]) * 3600 + int(time_array[2]) * 60 + int(time_array[4])
    except:
        print("Error in <revise.getTimeStringAsInt()>: string: " + time_string)
        return -1


def checkModuleAnswers(module):
    '''This function takes the module object and checks the answers of the given form submission'''
    return checkChildren(dict(), 0, module)


def checkChildren(results, count, point):
    for item in point._getChildren():
        if type(item) == Heading or (type(item) == Point and not item.isDisabled()):
            results, count = checkChildren(results, count, item)
    if (type(point) == Point and not point.isRoot) or (type(point) == Point and point.blankFill and point.isRoot):
        if not (point.blankFill and point.answer() == ""):
            results[point.id] = request.form.get(f"{point.id}")
    if type(point) == Point and point.checkAnswer(request.form.get(f"{point.id}")):
        if not (point.blankFill and point.answer() == ""):
            count += 1
    return (results, count)