from collections import namedtuple

from flask import current_app, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from lin.exception import InvalidTokenException, ExpiredTokenException

# auth = HTTPBasicAuth()
auth = HTTPTokenAuth()
User = namedtuple('User', ['id'])

@auth.verify_token
def verify_password(token):
    user_info = verify_auth_token(token)
    if not user_info:
        return False
    else:
        g.user = user_info
        return True

def verify_auth_token(token):
    # 验证token
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature:
        raise InvalidTokenException()
    except SignatureExpired:
        raise ExpiredTokenException()
    return User(data['id'])