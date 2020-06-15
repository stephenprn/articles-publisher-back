from models.user import User
from shared.db import db
from shared.annotations import to_json


def init_users():
    admin_exists = db.session.query(
        db.session.query(User).filter_by(username='admin').exists()
    ).scalar()

    if admin_exists:
        return

    admin = User('admin', 'admin@admin.com')

    db.session.add(admin)
    db.session.commit()


@to_json()
def get_users_list(nbr_results: int, page_nbr: int):
    users = User.query.order_by(User.creation_date).all()

    return [user.to_dict() for user in users]
