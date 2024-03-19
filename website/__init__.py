from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_migrate import Migrate
from os import getenv

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv("SECRET_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECURITY_PASSWORD_SALT"] = getenv("SECURITY_PASSWORD_SALT")
    db.init_app(app)
    migrate = Migrate(app, db)

    from .auth.auth import auth
    from .home.home import home
    from .create.create import create
    from .revise.revise import revise

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(home)
    app.register_blueprint(create, url_prefix="/create")
    app.register_blueprint(revise, url_prefix="/revise")

    from .models import User
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    create_database(app)

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print("Created database!")


def get_current_nav():
    navs = ["create", "revise", "login", "signup"] # Otherwise: home.
    current = "home"
    for nav in navs:
        if nav in request.path:
            current = nav
    return dict(current_nav = current)