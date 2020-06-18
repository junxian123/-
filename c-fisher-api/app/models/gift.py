"""
    create by xian on 2019/4/22
"""
from flask import current_app
from lin import db

from sqlalchemy import Column, Integer, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship

from app.models.base import Base
from app.models.consumer import Consumer


class Gift(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    consumer = relationship('Consumer')
    uid = Column(Integer, ForeignKey('consumer.id'))
    launched = Column(Boolean, default=False)
    book = relationship('Book')
    bid = Column(Integer, ForeignKey('book.id'))

    def __init__(self, uid=None, bid=None):
        self.uid = uid
        self.bid = bid

    def save_of_gift(self):
        with db.auto_commit():
            consumer = Consumer.get_consumer(self.uid)
            consumer.beans += current_app.config['BEAN_NUMBER']
            db.session.add(self)

    def cancel(self):
        gift = Gift.query.filter_by(uid=self.uid, bid=self.bid, launched=False, soft=True).first_or_404()
        consumer = Consumer.get_consumer(self.uid)
        consumer.beans -= current_app.config['BEAN_NUMBER']
        gift.delete(True)


    @classmethod
    def get_gifts_of_self(cls, uid):
        return cls.query.filter_by(uid=uid, launched=False, soft=True).order_by('-create_time').all()

    @classmethod
    def get_gifted_count(cls):
        s = db.session.query(
            func.count(cls.bid).label('count'), cls.bid).filter_by(
            launched=False, soft=True).group_by(cls.bid).distinct().all()
        return s

    @classmethod
    def get_gifts_by_bid(cls, bid):
        gifts = cls.query.filter_by(bid=bid, launched=False, soft=True).order_by().all()
        return gifts

    @classmethod
    def is_gifter(cls, bid, uid):
        return True if cls.query.filter_by(
            bid=bid, uid=uid, launched=False, soft=True).first() else False