from flask import request, g,jsonify
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.token_auth import auth
from app.models.mail import Mail

mail_api = Redprint('mail')


@mail_api.route('/save', methods=['POST'])
@auth.login_required
def save():
    uid = g.user.id
    mail = Mail.get(uid)
    if not mail:
        mail = Mail()
    data = request.json
    data['uid'] = uid
    mail.set_attrs(data)
    mail.save()
    return Success()


@mail_api.route('', methods=['GET'])
@auth.login_required
def get():
    uid = g.user.id
    mail = Mail.get(uid)
    return jsonify(mail), 200