from flask import Blueprint, request, flash, render_template, redirect, url_for, session
from flask_login import current_user, login_required
from ..models import db, Course, Module, Heading, Point

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


@create.route("/<int:id>")
@login_required
def tree(id):
    '''This page displays the creation tree of the course referenced by the given id.'''
    # db.session.delete(Point.query.get(1))
    # db.session.commit()
    course = Course.query.filter_by(id=id, user=current_user.id).first()
    if not course:
        flash("Invalid details!", category="error")
        return redirect(url_for("home.index"))
    session["course"] = id
    return render_template("tree.html", user=current_user, course=course, m=request.args.get("m"), h=request.args.get("h"))


@create.route("/add_module", methods=["GET", "POST"])
@login_required
def add_module():
    '''This page allows the user to add a module to the given course (in session).'''
    course = Course.query.filter_by(id=session["course"], user=current_user.id).first()
    if not course:
        flash("Invalid details!", category="error")
        return redirect(url_for("home.index"))
    if request.method == "POST":
        module = Module(
            name = request.form.get("name"),
            course = course.id
        )
        db.session.add(module)
        db.session.commit()
        flash("Module added!", category="success")
        return redirect(url_for("create.tree", _anchor=module.id, id=course.id))
    return render_template("add_module.html", user=current_user, course=course)


@create.route("/add_heading", methods=["GET", "POST"])
@login_required
def add_heading():
    '''This page allows the user to add a heading to the given module.'''
    module = Module.query.filter_by(id=request.args.get("m")).first()
    if not module or module.getCourse().user != current_user.id:
        flash("Invalid details!", category="error")
        return redirect(url_for("home.index"))
    course = module.getCourse()
    if request.method == "POST":
        heading = Heading(
            text = request.form.get("text"),
            module = module.id
        )
        db.session.add(heading)
        db.session.commit()
        flash("Heading added!", category="success")
        return redirect(url_for("create.tree", _anchor=heading.id, id=course.id))
    return render_template("add_heading.html", user=current_user, course=course, module=module)


def deletePoint(point):
    '''Recursively deletes the children of the given point, then deletes the point.'''
    if len(point.getChildren()) > 0:
        for child in point.getChildren():
            deletePoint(child)
    db.session.delete(point)


@create.route("/edit_tree", methods=["POST"])
@login_required
def edit_tree():
    '''This method handles the form submission when the user edits the tree (add child/sibling, delete node).'''
    if "Delete" in request.form or "Disable" in request.form or "Enable" in request.form:
        if request.form.get("parent_type") == "point":
            p = Point.query.get(int(request.form.get("id")))
            anchor = p.getHeading().id
        else:
            p = Heading.query.get(int(request.form.get("id")))
            anchor = p.id
        if not p:
            flash("Invalid details!", category="error")
            return redirect(url_for("create.index"))
        course = p.getCourse()
        heading = p.getHeading()
        module = heading.getModule()
        if "Delete" in request.form:
            deletePoint(p)
        elif "Disable" in request.form:
            p.disabled = True
        else:
            p.disabled = False
        db.session.commit()
    elif request.form.get("title") == "Edit":
        p = Point.query.get(int(request.form.get("id")))
        anchor=p.id
        if not p:
            flash("Invalid details!", category="error")
            return redirect(url_for("create.index"))
        course = p.getCourse()
        heading = p.getHeading()
        module = heading.getModule()

        blankFill = True
        if request.form.get("blank_fill") == "No":
            blankFill = False
        numeric = True
        if request.form.get("numeric") == "No":
            numeric = False
        punc = True
        if request.form.get("punctuation") == "No":
            punc = False
        code = True
        if request.form.get("code") == "No":
            code = False

        p.text = request.form.get("text")
        p.blankFill = blankFill
        p.hint = request.form.get("hint")
        p.numeric = numeric
        p.punc = punc
        p.code = code
        p.leniency = int(request.form.get("leniency"))
        db.session.commit()

    elif request.form.get("title") == "Add Child":
        # Check if this is a root or not.

        if request.form.get("parent_type") == "point":
            p = Point.query.get(int(request.form.get("id")))
        else:
            p = Heading.query.get(int(request.form.get("id")))
        if not p:
            flash("Invalid details!", category="error")
            return redirect(url_for("create.index"))
        course = p.getCourse()
        blankFill = True
        if request.form.get("blank_fill") == "No":
            blankFill = False
        numeric = True
        if request.form.get("numeric") == "No":
            numeric = False
        punc = True
        if request.form.get("punctuation") == "No":
            punc = False
        code = True
        if request.form.get("code") == "No":
            code = False
        isRoot = False
        if request.form.get("parent_type") == "heading":
            isRoot = True

        point = Point(
            text = request.form.get("text"),
            blankFill = blankFill,
            hint = request.form.get("hint"),
            parent = p.id,
            isRoot = isRoot,
            numeric = numeric,
            punc = punc,
            code = code,
            leniency = int(request.form.get("leniency"))
        )
        db.session.add(point)
        db.session.commit()
        anchor = point.id
        heading = point.getHeading()
        module = heading.getModule()
    elif request.form.get("title") == "Add Sibling":
        
        sibling = Point.query.get(int(request.form.get("id")))

        if not sibling:
            flash("Invalid details!", category="error")
            return redirect(url_for("create.index"))
        course = sibling.getCourse()
        blankFill = True
        if request.form.get("blank_fill") == "No":
            blankFill = False
        numeric = True
        if request.form.get("numeric") == "No":
            numeric = False
        punc = True
        if request.form.get("punctuation") == "No":
            punc = False
        code = True
        if request.form.get("code") == "No":
            code = False

        point = Point(
            text = request.form.get("text"),
            blankFill = blankFill,
            hint = request.form.get("hint"),
            parent = sibling.parent,
            isRoot = sibling.isRoot,
            numeric = numeric,
            punc = punc,
            code = code,
            leniency = int(request.form.get("leniency"))
        )
        db.session.add(point)
        db.session.commit()
        anchor = point.id
        heading = point.getHeading()
        module = heading.getModule()
    else:
        flash("Invalid details!", category="error")
        return redirect(url_for("create.index"))
    return redirect(url_for("create.tree", id=course.id, _anchor=anchor, m=module.id, h=heading.id))


# @create.route("/add_point", methods=["GET", "POST"])
# @login_required
# def add_point():
#     try:
#         parent_type = "point"
#         if request.args.get("heading"):
#             parent_type = "heading"
#             parent = Heading.query.filter_by(id=int(request.args.get(parent_type))).first()
#         else:
#             parent = Point.query.filter_by(id=int(request.args.get(parent_type))).first()
#         if not parent:
#             flash("Invalid details!", category="error")
#             return redirect(url_for("home.index"))
        
#         course = parent.getCourse()
        
#         if request.method == "POST":
#             blankFill = True
#             if request.form.get("blank_fill") == "No":
#                 blankFill = False
#             numeric = True
#             if request.form.get("numeric") == "No":
#                 numeric = False
#             isRoot = False
#             if parent_type == "heading":
#                 isRoot = True
#             point = Point(
#                 text = request.form.get("text"),
#                 blankFill = blankFill,
#                 hint = request.form.get("hint"),
#                 parent = parent.id,
#                 isRoot = isRoot,
#                 numeric = numeric
#             )
#             db.session.add(point)
#             db.session.commit()
#             flash("Point Added!", category="success")
#             return redirect(url_for("create.tree", _anchor=point.id, id=course.id))
        
#         return render_template("add_point.html", user=current_user, parent=parent, parent_type=request.args, course=course)
#     except Exception as e: # request.args.get("") may not give back an int.
#         flash("Invalid details!", category="error")
#         print(e)
#         return redirect(url_for("home.index"))


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