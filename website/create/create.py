from flask import Blueprint, request, flash, render_template, redirect, url_for
from flask_login import current_user, login_required
from ..models import db, Course

create = Blueprint("create", __name__, template_folder="templates", static_folder="static")


@create.route("/", methods=["GET", "POST"])
@login_required
def index():
    '''This page lists the courses that the user has currently created and allows them to modify/add new'''
    if request.method == "POST":
        db.session.add(Course(
            name = request.form.get("name"),
            user = current_user.id
        ))
        db.session.commit()
        flash("Course added.", category="success")
    return render_template("create.html", user=current_user)


# Create course
# Create module
# Create heading
# Create points (under the heading, or other points)

'''
Design Planning:
 - Aim is to be very easy to use and navigate levels.
 - Consider a tree structure.
    - Perhaps show all points under a heading?
    - Or alterntively, show all children that are on the current level, or one level below?
    - For example, when at root, the all courses and headings can be viewed.
    - At the bottom of each level, a link to "add" is displayed.
 - Perhaps also consider adding a "progress-bar" style feature at the top to show the tree navigation.
    - This will list all parent nodes (for example: Warwick CS | Sorting | CS126 | Merge Sort | [current point])
'''