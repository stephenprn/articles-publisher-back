from flask import Flask

from shared.db import db


def create_app():
    """Construct the core application."""
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///application.db"

    db.init_app(app)

    with app.app_context():
        # blueprints init
        from routes.application_auth import application_auth
        from routes.application_admin import application_admin

        app.register_blueprint(application_auth, url_prefix="/auth")
        app.register_blueprint(application_admin, url_prefix="/admin")

        db.create_all()  # Create sql tables for our data models

        return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)