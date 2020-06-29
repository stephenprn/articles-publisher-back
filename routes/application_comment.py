from flask import Blueprint, request, Response
from flask_jwt import jwt_required

from services import service_comment
from shared.annotations import pagination

application_comment = Blueprint("application_comment", __name__)


@application_comment.route("/comment-article/<art_url>", methods=["POST"])
@jwt_required()
def comment_article(art_url: str):
    body = request.form.get("body")

    service_comment.comment_article(body, art_url)

    return Response(status=204)

@application_comment.route("/comments-list/<art_url>")
@pagination(20)
def get_comments_list(art_url: str, nbr_results: int, page_nbr: int):
    return service_comment.get_comments_list(art_url, nbr_results, page_nbr)