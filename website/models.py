from . import db
from flask_login import UserMixin
import string
from sqlalchemy.sql import func
from fuzzywuzzy import fuzz


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(256))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    status = db.Column(db.String(64), default="user")

    def getCourses(self):
        '''Returns a list of the user's courses.'''
        return Course.query.filter_by(user=self.id).all()


class Course(db.Model): # Example: Warwick Computer Science - Year 1
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(512))
    user = db.Column(db.Integer, db.ForeignKey("user.id"))

    def getModules(self):
        '''Returns a list of the course's modules.'''
        return sorted(Module.query.filter_by(course=self.id).all(), key=lambda i: i.code)
    
    def getAttempts(self):
        '''Returns the integer number of revision attempts for the course.'''
        return 0 # WIP
    

class Module(db.Model): # Example: CS126 -> Design of Information Structures
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(16))
    name = db.Column(db.String(512))
    course = db.Column(db.Integer, db.ForeignKey("course.id"))
    attempts = db.Column(db.Integer, default=0)
    time = db.Column(db.String(128))

    def getHeadings(self):
        '''Returns a list of the modules's headings.'''
        return Heading.query.filter_by(module=self.id).all()
    
    def getCourse(self):
        '''Returns the Module's Course object.'''
        return Course.query.filter_by(id=self.course).first()
    
    def _getChildren(self):
        return self.getHeadings()


class Heading(db.Model): # Example: Sorting Algorithms
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(512))
    module = db.Column(db.Integer, db.ForeignKey("module.id"))
    attempts = db.Column(db.Integer, default=0)
    time = db.Column(db.String(128))
    order = db.Column(db.Integer, default=0)

    # def getAllPoints(self):
    #     '''This method returns an array of all points under the Heading object.'''
    #     item = self
    #     points = []
    #     for i in item._getChildren():
    #         points.append(i)

    # def getChildrenOfPoint(self, point):



    def getPoints(self):
        '''Returns a list of the Heading's Point objects'''
        return Point.query.filter_by(isRoot=True, parent=self.id).all()
    
    def getModule(self):
        '''Returns the Heading's Module object.'''
        return Module.query.filter_by(id=self.module).first()
    
    def getCourse(self):
        '''Returns the Course object for the Heading.'''
        return self.getModule().getCourse()
    
    def _getChildren(self):
        return self.getPoints()


class Point(db.Model): # Examples: [Merge Sort, Has a running time of O(n log n)]
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(1048576))
    blankFill = db.Column(db.Boolean) # If True, then this point can be used in "fill-the-blank" style questions.
    hint = db.Column(db.String(4096)) # Available to be shown (for example, "list 3 advantages")
    parent = db.Column(db.Integer) # If isRoot==True, then this points to a heading. Otherwise to another point.
    isRoot = db.Column(db.Boolean) # Can this be a starting point for a question (list the points below this one)?
    numeric = db.Column(db.Boolean, default=False) # If numeric, use <ol>, otherwise use <ul>
    punc = db.Column(db.Boolean, default=False) # Check punctuation when marking answers.
    leniency = db.Column(db.Integer, default=90) # Match percentage between given answer and correct answer.
    code = db.Column(db.Boolean, default=False) # Question requires code answer. Punc is overriden to False and a textarea is displayed instead of a standard 1-line input.
    disabled = db.Column(db.Boolean, default=False)
    successes = db.Column(db.Integer, default=0)
    failures = db.Column(db.Integer, default=0)
    last_answered = db.Column(db.DateTime(timezone=True))
    order = db.Column(db.Integer, default=0)
    
    def getChildren(self):
        '''Returns a list of Points of all children nodes for the Point.'''
        return Point.query.filter_by(isRoot=False, parent=self.id).all()
    
    def _getChildren(self):
        return self.getChildren()
    
    def getCourse(self):
        '''Returns the Point's Course object'''
        return self.getHeading().getCourse()
    
    def getHeading(self):
        '''Returns the Point's Heading object'''
        if self.isRoot:
            heading = Heading.query.filter_by(id=self.parent).first()
        else:
            point = self
            while point.isRoot == False:
                point = Point.query.filter_by(id=point.parent).first()
            heading = Heading.query.filter_by(id=point.parent).first()
        return heading
    
    def getParent(self):
        '''Returns the point's parent (Heading or Point)'''
        if self.isRoot:
            return Heading.query.get(self.parent)
        return Point.query.get(self.parent)
    
    def checkAnswer(self, answer):
        '''Strips punctuation and make lower case. Then compares the answer string to the point's text.'''
        return self._compareAnswers(formatString(answer, self.punc))
    
    def _compareAnswers(self, userAnswer):
        '''Returns True if the user's answer is within the accepted range of the point's answer, False otherwise.'''
        return fuzz.ratio(userAnswer, formatString(self.answer(), self.punc)) >= self.leniency
    
    def format(self):
        '''If the point is blank-fill capable, it returns the default string.'''
        if self.blankFill:
            return str(self.text).replace(">|<", "")
        return self.text
    
    def question(self):
        '''If the point is blank-fill capable, it returns just the question string'''
        try:
            return str(self.text)[0: str(self.text).index(">|<")]
        except Exception as e:
            # print("Error: " + str(e) + " : " + self.text)
            return self.text
    
    def answer(self):
        '''If the point is blank-fill capable, it returns just the answer string'''
        if not self.blankFill:
            return self.text
        try:
            return str(self.text)[str(self.text).index(">|<") + 4 : len(self.text)]
        except:
            return ""
        
    def isDisabled(self):
        '''Returns True if this node, or any parent node is marked as disabled, False otherwise.'''
        if self.disabled:
            return True
        if not self.isRoot:
            return self.getParent().isDisabled()
        return False
    
    def serialise(self):
        '''Returns a dictionary of all attributes for the Point object.'''
        return {
            "id": self.id,
            "text": self.text,
            "blankFill": str(self.blankFill),
            "hint": self.hint,
            "parent": self.parent,
            "isRoot": str(self.isRoot),
            "numeric": str(self.numeric),
            "punc": str(self.punc),
            "leniency": self.leniency,
            "code": str(self.code),
            "disabled": str(self.disabled),
            "successes": self.successes,
            "failures": self.failures,
            "last_answered": str(self.last_answered),
            "order": str(self.order)
        }
    
    def isTitle(self):
        if self.blankFill and ">|<" not in self.text:
            return True
        return False

    
def formatString(text, punc=False):
    '''Returns the given string in lower case w/o punctuation.'''
    # Remove puncuation. Source: https://stackoverflow.com/questions/265960/best-way-to-strip-punctuation-from-a-string (11/03/2024, from CS133 revision project) and https://stackoverflow.com/questions/8270092/remove-all-whitespace-in-a-string (04/05/2024).
    if not punc:
        # Remove puncutiaton, since it isn't being examined.
        return " ".join(str(text).lower().split()).translate(str.maketrans('', '', string.punctuation))
    return " ".join(str(text).lower().split())
