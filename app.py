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
# - Ability to toggle some leniency when answering questions 
#       (enter numeric percentage, default as 90%).
# - Properly select course, module, and heading to revise from.
# - When revising, can choose one of three modes: full text, 
#       random points (+count), or random blank-fill (+count).
# - Ability to type code in a textbox.
# - Point ordering
# - Add the option for adding parent node (change arrows).
# - Add ability to "hide" or "disable" certain nodes:
#   - Will not show in revision section.
#   - Greyed out in creation tree.
# - Fix spacing for points (Children all equidistant, sibling of parent has more spacing).
# - Fix empty answers ("Internet Protocols", for example).