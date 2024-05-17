from flask import redirect, url_for, flash
from website import create_app, get_current_nav

app = create_app()

@app.route("/")
def home():
    return redirect(url_for("home.index"))

@app.errorhandler(404)
def error_404(e):
    flash("That page doesn't exist. Redirecting to the home page...", category="error")
    return redirect(url_for("home.index"))

@app.context_processor
def current_nav():
    return get_current_nav()

if __name__ == "__main__":
    app.run(debug=True)

# Pending features:
# - Support for in-line Latex (both in creation tree and when typing revision).
# - When revising, can choose one of three modes: full text, random points (+count), or random blank-fill (+count).
# - Ability to type code in a textbox.
# - Point ordering
# - Add the option for adding parent node (change arrows).
# - Tree Keyboard Traversability:
#   - When "enter" is clicked on create tree, open form to add new SIBLING to last node (maybe last added?).
#   - When "tab" is clicked on create tree, open form to add new CHILD to last node (maybe last added?).
#   - When either is pressed, get ID from URL (as anchor), or add from LAST open point, and if not open, either (nothing or open and add to end of last module).
# - Pause timer and time override features.


# UPDATES:
# - Combine this code with previous note maker plans.
# - Lecture note-making.
# - Setting defitions in a glossary-type feature.
# - Links between sections.
# - Image insertion (with captions).
# - Revision schedule (multiple times through learning content (with progressively smaller and smaller hints), 
#       until eventually content is learned (counts hint increase and skip count)
# - Include definitions page
# - Includes "tell me about" pages, where the user is given a blank input and must
#       write everything they remember about the given topic.