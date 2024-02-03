from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(256))
    status = db.Column(db.String(64), default="user")


class Course(db.Model): # Example: Warwick Computer Science
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    user = db.Column(db.Integer, db.ForeignKey("user.id"))
    

class Module(db.Model): # Example: CS126 -> Design of Information Structures
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    course = db.Column(db.Integer, db.ForeignKey("course.id"))
    attempts = db.Column(db.Integer, default=0)


class Heading(db.Model): # Example: Sorting Algorithms
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512))
    module = db.Column(db.Integer, db.ForeignKey("module.id"))
    attempts = db.Column(db.Integer, default=0)


class Point(db.Model): # Examples: [Merge Sort, Has a running time of O(n log n)]
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1048576))
    hint = db.Column(db.String(4096)) # Available to be shown (for example, "list 3 advantages")
    parent = db.Column(db.Integer, db.ForeignKey("point.id"))
    isRoot = db.Column(db.Boolean) # Can this be a starting point for a question (list the points below this one)?
    successes = db.Column(db.Integer, default=0)
    failures = db.Column(db.Integer, default=0)
    last_answered = db.Column(db.DateTime(timezone=True))