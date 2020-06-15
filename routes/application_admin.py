from flask import Blueprint
from json import dumps

from services import service_admin
from shared.annotations import pagination

application_admin = Blueprint("application_admin", __name__)

service_admin.init_users()


@application_admin.route("/")
def hello():
    return "hello admin"


@application_admin.route("/users-list")
@pagination(20)
def get_users_list(nbr_results: int, page_nbr: int):
    return service_admin.get_users_list(nbr_results, page_nbr)
