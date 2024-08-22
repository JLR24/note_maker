# # # # # # # # # # # # # # #
# Jack Ricketts
# 04/08/2024, 17:25 (BST+1)
# UniAssist Point Exporter
# # # # # # # # # # # # # # #

from ...models import Point

class Marker():
    def __init__(self, leniency, equation, markBrackets, markPunc, markSpaces, markCase, markNumbers, point):
    # id field
        self.leniency = leniency # Double
        self.equation = equation # Bool
        self.markBrackets = markBrackets # Bool
        self.markPunc = markPunc # Bool
        self.markSpaces = markSpaces # Bool
        self.markCase = markCase # Bool
        self.markNumbers = markNumbers # Bool
        self.point = point # ExportPoint (leave blank and handle at other end?)

class ExportPoint():
    def __init__(self, text, hint, note, answer, root, parent, heading, headingID, disabled, blankFill, title, order, marker, points):
        # id field
        self.text = text # String
        self.hint = hint # String
        self.note = note # String
        self.answer = answer # String
        self.root = root # Bool
        self.parent = parent # Point (leave blank and handle at other end?)
        self.heading = heading # Heading (leave blank and handle at other end?)
        self.headingID = headingID # UUID (leave blank and handle at other end?)
        self.disabled = disabled # Bool
        self.blankFill = blankFill # Bool
        self.title = title # Bool
        self.order = order # Int
        self.marker = marker # Marker
        self.points = points # [ExportPoint]


def export(points):
    return convert(points)


def convert(points):
    '''This method takes the array of point objects for the specified heading and exports them as required.'''
    result = []
    for point in points:
        result.append(convertPoint(point))
    return result


def convertPoint(point: Point):
    '''This method returns the JSON equivalent of the given point'''
    return {
        "text": point.question(),
        "hint": point.hint,
        "note": "", # OR DO I MAKE THIS POINT.HINT?
        "answer": point.answer(),
        "root": point.isRoot,
        "disabled": point.disabled,
        "blankFill": point.blankFill,
        "title": point.isTitle(),
        "order": point.order,
        "marker": convertMarker(point),
        "points": convert(point.getChildren())
    }

def convertMarker(point: Point):
    return {
        "leniency": point.leniency,
        "equation": point.code,
        "markBrackets": True,
        "markPunc": point.punc,
        "markSpaces": False,
        "markCase": False,
        "markNumbers": False,
        # Missing point
    }