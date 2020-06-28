from sqlalchemy.orm import load_only

from models.user import User, UserRole
from shared.db import db
from shared.annotations import to_json


def init_users():
    admin_exists = db.session.query(User.id).filter_by(
        username='admin').scalar() is not None

    if admin_exists:
        return

    admin = User('admin', 'admin@admin.com', 'password', UserRole.admin)

    db.session.add(admin)
    db.session.commit()


@to_json(paginated=True)
def get_users_list(nbr_results: int, page_nbr: int):
    res = db.session.query(User).options(load_only(
        'uuid',
        'email',
        'username',
        'creation_date'
    )).order_by(
        User.creation_date
    ).paginate(
        page=page_nbr,
        per_page=nbr_results,
        error_out=False
    )

    return {
        'total': res.total,
        'data': res.items
    }
