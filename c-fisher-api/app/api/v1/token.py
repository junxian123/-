from lin.redprint import Redprint
from flask import jsonify

from app.models.consumer import Consumer
from app.validators.forms import WXLoginForm

token_api = Redprint('token')

@token_api.route('', methods=['POST'])
def get_token():
    form = WXLoginForm().validate_for_api()
    access_token = Consumer.login(form)
    return jsonify({
        'access_token': access_token
    })
