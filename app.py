from flask import Flask
from flask_cors import CORS
from flask_jwt import JWT

from os import environ
from werkzeug.exceptions import HTTPException
from json import dumps
from dotenv import load_dotenv

from shared.db import db
from services.service_admin import init_users
from services.service_auth import authenticate, identity


def create_app():
    """Load env parameters"""
    load_dotenv()

    """Construct the core application."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get(
        "SQLALCHEMY_DATABASE_URI")
    app.config["SECRET_KEY"] = environ.get("SECRET_KEY")
    app.config["JWT_AUTH_URL_RULE"] = environ.get("JWT_AUTH_URL_RULE")
    app.config["JWT_AUTH_USERNAME_KEY"] = environ.get("JWT_AUTH_USERNAME_KEY")

    db.init_app(app)

    with app.app_context():
        # blueprints init
        from routes.application_auth import application_auth
        from routes.application_article import application_article
        from routes.application_comment import application_comment

        app.register_blueprint(application_auth, url_prefix="/auth")
        app.register_blueprint(application_article, url_prefix="/article")
        app.register_blueprint(application_comment, url_prefix="/comment")

        db.create_all()  # Create sql tables for our data models
        init_users()

        CORS(app)
        return app


app = create_app()
jwt = JWT(app, authenticate, identity)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    print(e)

    if isinstance(e, HTTPException):
        code = e.code

    try:
        return dumps(str(e.description)), code
    except Exception:
        return dumps(str(e)), code


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
