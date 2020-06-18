from flask import request, g, jsonify
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.token_auth import auth
from app.models.consumer import Consumer
from app.models.drift import Drift
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.count_gift import CountGift
from app.view_models.drift import DriftViewModel

drift_api = Redprint('drift')

@drift_api.route('/gift', methods=['POST'])
@auth.login_required
def save_of_drift_by_gift():
    # 通过向他人赠送书籍--送出书籍
    uid = g.user.id
    data = request.json

    book = data['book']
    # 对方-->接收者
    wish_id = data['wish_id']
    requester = Wish.query.get(wish_id).consumer
    # 我-->赠送者
    gifter = Gift.query.filter_by(soft=True, launched=False, uid=uid).first()

    drift = Drift(book=book, requester=requester, gifter=gifter)
    drift.save_drift()
    return Success()

@drift_api.route('/request', methods=['POST'])
@auth.login_required
def save_of_drift_by_request():
    # 通过向他人请求书籍
    uid = g.user.id
    data = request.json
    drift_id = data['drift_id']
    mail = data['mail']
    message = data['message']
    # 我-->接受者
    requester = Consumer.get_consumer(uid)
    if drift_id:
        drift = __set_of_drift_by_did(drift_id=drift_id, mail=mail, message=message)
    else:
        book = data['book']
        # 对方-->赠送者
        gift_id = data['gift_id']
        gifter = Gift.query.get(gift_id)
        drift = Drift(book=book, requester=requester, gifter=gifter, mail=mail, message=message)
    # 鱼豆-1
    requester.beans -= 1
    drift.save_drift()
    return Success()

@drift_api.route('/my/received')
@auth.login_required
def get_received_drift_of_my():
    # 自己收到鱼漂
    uid = g.user.id
    drifts = Drift.get_received_drift_of_my(uid)
    drifts = [DriftViewModel(drift) for drift in drifts]
    return jsonify(drifts), 200


@drift_api.route('/my/sent')
@auth.login_required
def get_sent_drift_of_my():
    # 自己赠送出去的鱼漂
    uid = g.user.id
    drifts = Drift.get_sent_drift_of_my(uid)
    drifts = [DriftViewModel(drift) for drift in drifts]
    return jsonify(drifts), 200

@drift_api.route('/cancel/<int:did>',methods=['GET'])
@auth.login_required
def cancel_drift(did):
    uid = g.user.id
    Drift.cancel_drift(uid=uid, did=did)
    return Success()



@drift_api.route('/mail/<int:did>', methods=['GET'])
@auth.login_required
def mail_drift(did):
    uid = g.user.id
    Drift.mail_drift(uid=uid, did=did)
    return Success()

@drift_api.route('/reject/<int:did>', methods=['GET'])
@auth.login_required
def reject_mail(did):
    uid = g.user.id
    Drift.reject_drift(uid=uid, did=did)
    return Success()

@drift_api.route('/delete/<int:did>', methods=['GET'])
@auth.login_required
def delete_mail(did):
    Drift.delete_mail(did)
    return Success()

@drift_api.route('/count_gift', methods=['GET'])
@auth.login_required
def count_gifted():
    uid = g.user.id
    data = Drift.count_gift(uid=uid)
    res = [CountGift(item) for item in data]
    return jsonify(res), 200


def __set_of_drift_by_did(drift_id=None, mail=None, message=None):
    drift = Drift.get_drift(drift_id)
    drift.recipient_name = mail['nickname']
    drift.mobile = mail['mobile']
    drift.address = mail['province']+mail['city']+mail['address']
    drift.message = message
    return drift


