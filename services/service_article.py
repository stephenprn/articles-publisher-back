from flask import abort
from sqlalchemy.orm import load_only, joinedload

from models.user import User
from models.article import Article
from utils.utils_string import normalize_string
from shared.db import db
from shared.annotations import to_json
from flask_jwt import current_identity

URL_SEPARATOR = "-"
MIN_LENGTH_TITLE = 8


def add_article(title: str, body: str = None):
    if title == None or len(title) < MIN_LENGTH_TITLE:
        abort(400, "Article title must be at least {} characters long".format(
            str(MIN_LENGTH_TITLE)))

    article = Article(title, body=body)
    article.url = generate_unique_url(title)
    article.user = current_identity

    db.session.add(article)
    db.session.commit()


@to_json(paginated=True)
def get_articles_list(nbr_results: int, page_nbr: int):
    res = db.session.query(
        Article
    ).options(
        joinedload(
            Article.user
        ).load_only(
            "username"
        ),
        load_only(
            "title",
            "body",
            "url",
            "creation_date"
        )
    ).order_by(
        Article.creation_date
    ).paginate(
        page=page_nbr,
        per_page=nbr_results,
        error_out=False
    )

    return {
        "total": res.total,
        "data": res.items
    }


@to_json()
def get_article(url: str):
    article = db.session.query(Article).options(load_only(
        "title",
        "body"
    )).filter_by(
        url=url
    ).first()

    if article == None:
        abort(404, "Article not found")

    return article


def generate_unique_url(title: str):
    url_base = normalize_string(title, replace_spaces=URL_SEPARATOR)
    url = url_base

    url_index = 0

    while db.session.query(Article.id).filter_by(url=url).scalar() is not None:
        url_index += 1
        url = url_base + URL_SEPARATOR + str(url_index)

    return url
