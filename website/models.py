from . import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(256))
    status = db.Column(db.String(64), default="user")

    def getCourses(self):
        '''Returns a list of the user's courses.'''
        return Course.query.filter_by(user=self.id).all()


class Course(db.Model): # Example: Warwick Computer Science
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    user = db.Column(db.Integer, db.ForeignKey("user.id"))

    def getModules(self):
        '''Returns a list of the course's modules.'''
        return Module.query.filter_by(course=self.id).all()
    
    def getAttempts(self):
        '''Returns the integer number of revision attempts for the course.'''
        return 0 # WIP
    

class Module(db.Model): # Example: CS126 -> Design of Information Structures
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    course = db.Column(db.Integer, db.ForeignKey("course.id"))
    attempts = db.Column(db.Integer, default=0)

    def getHeadings(self):
        '''Returns a list of the modules's headings.'''
        return Heading.query.filter_by(module=self.id).all()
    
    def getCourse(self):
        '''Returns the Module's Course object.'''
        return Course.query.filter_by(id=self.course).first()


class Heading(db.Model): # Example: Sorting Algorithms
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512))
    module = db.Column(db.Integer, db.ForeignKey("module.id"))
    attempts = db.Column(db.Integer, default=0)


class Point(db.Model): # Examples: [Merge Sort, Has a running time of O(n log n)]
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1048576))
    blankFill = db.Column(db.Boolean) # If True, then this point can be used in "fill-the-blank" style questions.
    hint = db.Column(db.String(4096)) # Available to be shown (for example, "list 3 advantages")
    parent = db.Column(db.Integer) # If isRoot==True, then this points to a heading. Otherwise to another point.
    isRoot = db.Column(db.Boolean) # Can this be a starting point for a question (list the points below this one)?
    successes = db.Column(db.Integer, default=0)
    failures = db.Column(db.Integer, default=0)
    last_answered = db.Column(db.DateTime(timezone=True))