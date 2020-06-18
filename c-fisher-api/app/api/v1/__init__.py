"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint
from app.api.v1 import book, token, gift, wish, user, mail, drift


def create_v1():
    bp_v1 = Blueprint('v1', __name__)
    book.book_api.register(bp_v1)
    token.token_api.register(bp_v1)
    gift.gift_api.register(bp_v1)
    wish.wish_api.register(bp_v1)
    user.user_api.register(bp_v1)
    mail.mail_api.register(bp_v1)
    drift.drift_api.register(bp_v1)
    return bp_v1
