
from flask import abort
from flask_jwt import current_identity

from sqlalchemy.orm import load_only, joinedload
from sqlalchemy import desc

from models.comment import Comment
from models.article import Article
from shared.db import db
from utils.utils_string import check_length
from shared.annotations import to_json

COMMENT_MIN_LENGTH = 6
COMMENT_MAX_LENGTH = 600

@to_json(paginated=True)
def get_comments_list(url: str, nbr_results: int, page_nbr: int):
    res = db.session.query(
        Comment
    ).options(
        joinedload(
            Comment.user
        ).load_only(
            "username"
        ),
        load_only(
            "uuid",
            "body",
            "creation_date"
        )
    ).join(
        Article
    ).filter(
        Article.url==url
    ).order_by(
        desc(Comment.creation_date)
    ).paginate(
        page=page_nbr,
        per_page=nbr_results,
        error_out=False
    )

    return {
        "total": res.total,
        "data": res.items
    }


def comment_article(body: str, url: str):
    check_length(body, "Comment", COMMENT_MIN_LENGTH, COMMENT_MAX_LENGTH)

    article = db.session.query(Article).options(
        load_only(
            "id"
        )
    ).filter_by(
        url=url
    ).first()

    if article == None:
        abort(404, "Article not found")

    comment = Comment(body)
    comment.article = article
    comment.user = current_identity

    db.session.add(comment)
    db.session.commit()
