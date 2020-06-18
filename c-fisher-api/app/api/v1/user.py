from flask import request, g,jsonify
from lin import db
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.token_auth import auth
from app.models.consumer import Consumer

user_api = Redprint('user')


@user_api.route('/beans', methods=['GET'])
@auth.login_required
def get_beans():
    uid = g.user.id
    consumer = Consumer.get_consumer(uid)
    return jsonify(consumer.beans), 200


@user_api.route('/save', methods=['POST'])
@auth.login_required
def update():
    uid = g.user.id
    wx_nickname = request.json['nickname']
    consumer = Consumer.query.get_or_404(uid)
    with db.auto_commit():
        consumer.wx_name = wx_nickname
    return Success()

@user_api.route('/count', methods=['GET'])
@auth.login_required
def get_counter():
    uid = g.user.id
    consumer = Consumer.query.filter_by(uid).first()
    return jsonify({
        'receive_count': consumer.receive_counter,
        'send_count': consumer.send_counter
    })
