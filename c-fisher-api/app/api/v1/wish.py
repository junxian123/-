from flask import g, jsonify
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.token_auth import auth
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import MyTrade

wish_api = Redprint('wish')

@wish_api.route('/<bid>', methods=['GET'])
@auth.login_required
def save_of_wish(bid):
    uid = g.user.id
    wish = Wish(uid=uid, bid=bid)
    wish.save_of_wish()
    return Success()

@wish_api.route('/self', methods=['GET'])
@auth.login_required
def get_wishes_of_self():
    uid = g.user.id
    wishes = Wish.get_wishes_of_self(uid)
    trades_count_list = Gift.get_gifted_count()
    my_trade = MyTrade(wishes, trades_count_list)
    return jsonify(my_trade)

@wish_api.route('/cancel/<int:bid>', methods=['DELETE'])
@auth.login_required
def cancel(bid):
    uid = g.user.id
    wish = Wish(uid=uid, bid=bid)
    wish.cancel()
    return Success()