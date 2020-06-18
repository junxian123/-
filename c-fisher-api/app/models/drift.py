from flask import g
from lin import db
from sqlalchemy import Column, String, Integer, SmallInteger, desc, func

from lin.interface import InfoCrud as Base

from app.libs.enums import PendingStatus
from app.models.consumer import Consumer
from app.models.gift import Gift
from app.models.wish import Wish


class Drift(Base):
    """
        一次具体的交易信息
    """
    __tablename__ = 'drift'

    # 邮寄信息
    id = Column(Integer, primary_key=True, autoincrement=True)
    recipient_name = Column(String(20))
    address = Column(String(100))
    message = Column(String(200))
    mobile = Column(String(20))

    # 书籍信息
    bid = Column(Integer)
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # 请求者信息
    requester_id = Column(Integer)
    requester_nickname = Column(String(20))

    # 赠送者信息
    gifter_id = Column(Integer)
    gift_id = Column(Integer)
    gifter_nickname = Column(String(20))

    _pending = Column('pending', SmallInteger, default=1)

    def __init__(self, mail=None, book=None, requester=None, gifter=None, message=None):

        if mail:
            # 邮寄信息
            self.recipient_name = mail['nickname']
            self.address = mail['province'] + mail['city'] + mail['address']
            self.mobile = mail['mobile']

        if book:
            # 书籍信息
            self.bid = book['id']
            self.book_title = book['title']
            self.book_author = book['author']
            self.book_img = book['image']

        if requester:
            # 请求者信息
            self.requester_id = requester.id
            self.requester_nickname = requester.wx_name

        if gifter:
            # 赠送者信息
            self.gift_id = gifter.id
            self.gifter_id = gifter.consumer.id
            self.gifter_nickname = gifter.consumer.wx_name

        if message:
            # 留言
            self.message = message

    @property
    def pending(self):
        return PendingStatus(self._pending)

    @pending.setter
    def pending(self, status):
        self._pending = status.value

    def save_drift(self):
        with db.auto_commit():
            db.session.add(self)

    @classmethod
    def get_received_drift_of_my(cls, uid):
        return cls.query.filter_by(requester_id=uid, soft=True).order_by('-create_time').all()

    @classmethod
    def get_sent_drift_of_my(cls, uid):
        return cls.query.filter_by(gifter_id=uid, soft=True).order_by('-create_time').all()

    @classmethod
    def get_drift(cls, did):
        return cls.query.get(did)

    @classmethod
    def is_gifted_or_requested(cls, bid, gifter_id, request_id):
        return True if cls.query.filter(
            cls.bid == bid, cls.gifter_id == gifter_id,
            cls.requester_id == request_id, cls._pending != PendingStatus.Cancel.value
        ).first() else False

    @classmethod
    def is_gifter_or_requester(cls, drift_id):
        uid = g.user.id
        return 'gifter' if cls.query.filter_by(id=drift_id, gifter_id=uid, soft=True).first() else 'requester'

    @classmethod
    def cancel_drift(cls, uid=None, did=None):
        with db.auto_commit():
            requester = Consumer.get_consumer(uid)
            requester.beans += 1
            drift = cls.get_drift(did)
            drift.pending = PendingStatus.Cancel

    @classmethod
    def reject_drift(cls, uid=None, did=None):
        with db.auto_commit():
            drift = Drift.query.filter_by(id=did, gifter_id=uid, soft=True).first()
            drift.pending = PendingStatus.Reject
            if drift.address:
                requester = Consumer.get_consumer(drift.requester_id)
                requester.beans += 1

    @classmethod
    def mail_drift(cls, uid=None, did=None):
        with db.auto_commit():
            drift = Drift.query.filter_by(id=did, gifter_id=uid, soft=True).first()
            drift.pending = PendingStatus.Success

            wished = Wish.query.filter_by(uid=drift.requester_id, bid=drift.bid, launched=False, soft=True).first()
            if wished:
                wished.launched = True
            requester = Consumer.get_consumer(drift.requester_id)
            requester.update_receive_counter()

            gifted = Gift.query.filter_by(uid=drift.gifter_id, bid=drift.bid, launched=False, soft=True).first()
            gifted.consumer.update_send_counter()
            gifted.launched = True

    @classmethod
    def delete_mail(cls, did):
        drift = cls.query.get(did)
        if drift:
            drift.delete(commit=True)

    @classmethod
    def count_gift(cls, uid):
        return db.session.query(func.date_format(
            Drift.update_time, '%Y-%m-%d'
        ).label('time'), func.count(1)).filter_by(
            gifter_id=uid, _pending=PendingStatus.Success.value, soft=True
        ).group_by('time').order_by(desc('time')).distinct().all()
