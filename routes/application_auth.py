from flask import Blueprint

from shared.db import db

application_auth = Blueprint("application_auth", __name__)


@application_auth.route("/")
def hello():
    return "hello auth"