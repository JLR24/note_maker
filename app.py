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

    ## NEED TO INITIALIE GIT