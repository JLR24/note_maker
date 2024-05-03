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
# - Blank fill for child nodes.
# - Support for in-line Latex (both in creation tree and when typing revision).
# - Ability to toggle punctuation filter.
# - Ability to toggle some leniency when answering questions 
#       (enter numeric percentage, default as 90%).
# - Properly select course, module, and heading to revise from.
# - When revising, can choose one of three modes: full text, 
#       random points (+count), or random blank-fill (+count).
# Fix home page and explanation.
# Make timer visible wherever you are on the page.
# For full module/heading, store best time.
# Ability to type code in a textbox.
# The ability to edit a point (add extra button to display with pen icon, brings up form).
# Fix white-space stripping.