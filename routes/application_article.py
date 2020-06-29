from flask import Blueprint, request, Response
from flask_jwt import jwt_required

from services import service_article
from shared.annotations import pagination

application_article = Blueprint("application_article", __name__)


@application_article.route("/")
def hello():
    return "hello admin"


""" Articles lists """


@application_article.route("/my-articles-list")
@jwt_required()
@pagination(20)
def get_my_articles_list(nbr_results: int, page_nbr: int):
    return service_article.get_my_articles_list(nbr_results, page_nbr)


@application_article.route("/articles-list")
@pagination(20)
def get_articles_list(nbr_results: int, page_nbr: int):
    return service_article.get_articles_list(nbr_results, page_nbr)


""" Articles details """


@application_article.route("/article-details/<art_url>")
def get_article(art_url: str):
    return service_article.get_article(art_url)


@application_article.route("/my-article-details/<art_url>")
@jwt_required()
def get_my_article(art_url: str):
    return service_article.get_my_article(art_url)


""" Interact with articles """


@application_article.route("/add-article", methods=["POST"])
@jwt_required()
def add_article():
    title = request.form.get("title")
    body = request.form.get("body")

    service_article.add_article(title, body)

    return Response(status=204)


@application_article.route("/update-article/<art_url>", methods=["POST"])
@jwt_required()
def update_article(art_url: str):
    title = request.form.get("title")
    body = request.form.get("body")

    service_article.update_article(title, body, art_url)

    return Response(status=204)


@application_article.route("/delete-article/<art_url>", methods=["DELETE"])
@jwt_required()
def delete_article(art_url: str):
    service_article.delete_article(art_url)

    return Response(status=204)
