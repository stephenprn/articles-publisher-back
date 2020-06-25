from flask import Blueprint, request
from flask_jwt import jwt_required
from json import dumps

from shared.db import db
from services import service_auth

application_auth = Blueprint("application_auth", __name__)

# /login endpoint is reserved and managed by flask_jwt


@application_auth.route("/")
def hello():
    return "hello auth"


@application_auth.route("/register", methods=["POST"])
def register():
    email = request.json.get("email")
    username = request.json.get("username")
    password = request.json.get("password")

    service_auth.register(email, username, password)

    return dumps(True)


# this endpoint will return a 409 code if username is taken, 200 if not

@application_auth.route("/check-username", methods=["POST"])
def check_username():
    username = request.json.get("username")
    service_auth.check_username(username)

    return dumps(True)


# this endpoint will return a 401 code if token is invalid, 200 if valid

@application_auth.route("/check-logged")
@jwt_required()
def check_logged():
    return dumps(True)
