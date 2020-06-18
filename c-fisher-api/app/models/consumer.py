"""
    create by xian on 2019/4/22
"""


import requests
from flask import current_app
from lin import db
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, Float, Boolean, String

from app.libs.error_code import RefreshException
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Consumer(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(24), nullable=True)
    phone_number = Column(String(18), unique=True)
    _password = Column('password', String(128), nullable=True)
    email = Column(String(50), unique=True, nullable=True)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(50), default='未名')

    @classmethod
    def login(cls, form):
        consumer = cls.__get_consumer_info(form)
        # 保存用户信息
        openid = consumer['openid']
        consumer = cls.__save_consumer(openid)
        access_token = cls.__save_consumer_session(consumer.id, expiration=current_app.config['EXPIRATION'])
        return access_token

    @classmethod
    def __save_consumer(cls, openid):
        with db.auto_commit():
            consumer = Consumer.query.filter_by(wx_open_id=openid,soft=True).first()
            if consumer is None:
                consumer = Consumer()
                consumer.wx_open_id = openid
                db.session.add(consumer)
                db.session.flush()
            return consumer

    @classmethod
    def __save_consumer_session(cls, uid, expiration=7200):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

        return s.dumps({'id': uid}).decode('ascii')

    @classmethod
    def __get_consumer_info(cls, form):
        params = {
            'appid': current_app.config['APPID'],
            'secret': current_app.config['SECRET'],
            'js_code': form.code.data,
            'grant_type': 'authorization_code'
        }
        r = requests.get('https://api.weixin.qq.com/sns/jscode2session', params=params)
        try:
            return r.json()
        except:
            raise RefreshException()

    @staticmethod
    def get_consumer(uid):
        return Consumer.query.get_or_404(uid)

    def substract_beans(self):
        with db.auto_commit():
            self.beans -= 1

    def update_send_counter(self, commit=False):
        self.send_counter += 1
        if commit:
            with db.auto_commit():
                db.session.add(self)

    def update_receive_counter(self, commit=False):
        self.receive_counter += 1
        if commit:
            with db.auto_commit():
                db.session.add(self)