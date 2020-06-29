from flask import abort
from flask_jwt import current_identity
from sqlalchemy.orm import load_only, joinedload
from sqlalchemy import desc
import threading

from models.user import User
from models.article import Article
from utils.utils_string import normalize_string, check_length
from shared.db import db
from shared.annotations import to_json

URL_SEPARATOR = "-"
TITLE_MIN_LENGTH = 8
TITLE_MAX_LENGTH = 100


def add_article(title: str, body: str):
    check_length(title, "Article title", TITLE_MIN_LENGTH, TITLE_MAX_LENGTH)

    article = Article(title, body=body)
    article.url = __generate_unique_url(title)
    article.user = current_identity

    db.session.add(article)
    db.session.commit()

def update_article(title: str, body: str, url: str):
    check_length(title, "Article title", TITLE_MIN_LENGTH, TITLE_MAX_LENGTH)

    article = db.session.query(Article).options(
        joinedload(
            Article.user
        ).load_only(
            "username"
        ), load_only(
            "title",
            "body",
            "url",
            "creation_date"
        )
    ).filter_by(
        url=url,
        user_id=current_identity.id
    ).first()

    if article == None:
        abort(401, "Article not found")

    article.title = title
    article.body = body

    db.session.commit()


@to_json(paginated=True)
def get_my_articles_list(nbr_results: int, page_nbr: int):
    res = db.session.query(
        Article
    ).options(
        load_only(
            "title",
            "url",
            "creation_date",
            "nbr_views"
        )
    ).filter_by(
        user_id=current_identity.id
    ).order_by(
        desc(Article.creation_date)
    ).paginate(
        page=page_nbr,
        per_page=nbr_results,
        error_out=False
    )

    return {
        "total": res.total,
        "data": res.items
    }


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
            "url",
            "creation_date"
        )
    ).order_by(
        desc(Article.creation_date)
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
    article = db.session.query(Article).options(
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
    ).filter_by(
        url=url
    ).first()

    if article == None:
        abort(404, "Article not found")

    article.nbr_views += 1
    db.session.commit()

    # we don't want nbr_views to be sent to the user
    delattr(article, 'nbr_views')

    return article


@to_json()
def get_my_article(url: str):
    article = db.session.query(Article).options(
        load_only(
            "title",
            "body",
            "url",
            "creation_date"
        )
    ).filter_by(
        url=url,
        user_id=current_identity.id
    ).first()

    if article == None:
        abort(401, "Article not found")

    return article


def delete_article(url: str):
    article = db.session.query(Article).options(
        load_only(
            "id"
        )
    ).filter_by(
        url=url,
        user_id=current_identity.id
    ).first()

    if article == None:
        abort(401, "Article not found")

    db.session.delete(article)
    db.session.commit()


def __generate_unique_url(title: str):
    url_base = normalize_string(title, replace_spaces=URL_SEPARATOR)
    url = url_base

    url_index = 0

    while db.session.query(Article.id).filter_by(url=url).scalar() is not None:
        url_index += 1
        url = url_base + URL_SEPARATOR + str(url_index)

    return url
