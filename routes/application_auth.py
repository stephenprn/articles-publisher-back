from flask import Blueprint

from shared.db import db
from services import service_auth

application_auth = Blueprint("application_auth", __name__)
# /login route reserved for jwt authentication


@application_auth.route("/")
def hello():
    return "hello auth"

