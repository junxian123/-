"""
    create by xian on 2019/4/24
"""
from lin import db
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, ForeignKey, Boolean, func
from sqlalchemy.orm import relationship



class Wish(Base):
    id = Column(Integer, primary_key=True)
    consumer = relationship('Consumer')
    uid = Column(Integer, ForeignKey('consumer.id'))
    launched = Column(Boolean, default=False)
    book = relationship('Book')
    bid = Column(Integer, ForeignKey('book.id'))

    def __init__(self, uid=None, bid=None):
        self.uid = uid
        self.bid = bid


    def save_of_wish(self):
        with db.auto_commit():
            db.session.add(self)

    def cancel(self):
        wish = Wish.query.filter_by(uid=self.uid, bid=self.bid, launched=False, soft=True).first_or_404()
        wish.delete(True)




    @classmethod
    def get_wished_count(cls):
        return db.session.query(
            func.count(cls.bid).label('count'), cls.bid).filter_by(
            launched=False, soft=True).group_by(cls.bid).all()

    @classmethod
    def get_wishes_of_self(cls, uid):
        return cls.query.filter_by(uid=uid, launched=False, soft=True).all()


    @classmethod
    def get_wishes_by_bid(cls, bid):
        wishes = cls.query.filter_by(bid=bid, launched=False, soft=True).all()
        return wishes

    @classmethod
    def is_wisher(cls, bid, uid):
        return True if cls.query.filter_by(
            bid=bid, uid=uid, launched=False, soft=True).first() else False

