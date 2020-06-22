from flask import Blueprint
from flask_jwt import jwt_required
from json import dumps

from shared.db import db
from services import service_auth

application_auth = Blueprint("application_auth", __name__)


@application_auth.route("/")
def hello():
    return "hello auth"

# this endpoint will return a 401 code if token is invalid, 200 if valid


@application_auth.route("/check-logged")
@jwt_required()
def check_logged():
    return dumps(True)
