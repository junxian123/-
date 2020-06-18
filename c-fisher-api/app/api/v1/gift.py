from flask import g, jsonify, request, current_app
from lin.exception import Success

from app.libs.token_auth import auth
from lin.redprint import Redprint

from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import MyTrade

gift_api = Redprint('gift')

@gift_api.route('/save/<int:bid>', methods=['GET'])
@auth.login_required
def save_of_gift(bid):
    uid = g.user.id
    gift = Gift(bid=bid, uid=uid)
    gift.save_of_gift()
    return Success()

@gift_api.route('/cancel/<int:bid>', methods=['DELETE'])
@auth.login_required
def cancel(bid):
    uid = g.user.id
    gift = Gift(bid=bid, uid=uid)
    gift.cancel()
    return Success()

@gift_api.route('/recent', methods=['GET'])
def get_recently_upload():
    start = request.args['start']
    pre_page_count = current_app.config['PRE_PAGE_COUNT']
    recently_upload = Gift.paged_query(start, pre_page_count, soft=True, launched=False)
    books = [r_u.book for r_u in recently_upload]
    total = Gift.get_total(soft=True, launched=False)
    result = {
        'books': books,
        'total': total
    }
    return jsonify(result)

@gift_api.route('/self', methods=['GET'])
@auth.login_required
def get_gifts_of_self():
    uid = g.user.id
    gifts = Gift.get_gifts_of_self(uid)
    trades_count_list = Wish.get_wished_count()
    my_trade = MyTrade(gifts, trades_count_list)
    return jsonify(my_trade)

@gift_api.route('/occupant/<int:gid>', methods=['GET'])
@auth.login_required
def get_occupant(gid):
    # 获取书籍拥有者信息
    consumer = Gift.query.get(gid).consumer
    t = {
        'nickname': consumer.wx_name,
        'beans': consumer.beans,
        'receive_or_send': str(consumer.receive_counter) + '/' + str(consumer.send_counter)
    }
    return jsonify(t), 200
