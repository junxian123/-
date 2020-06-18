from lin import db
from lin.interface import InfoCrud as Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship


class Mail(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    nickname = Column(String(30), nullable=True)
    mobile = Column(String(16), nullable=True)
    province = Column(String(10), nullable=True)
    city = Column(String(10), nullable=True)
    address = Column(String(50), nullable=True)

    consumer = relationship('Consumer')
    uid = Column(Integer, ForeignKey('consumer.id'))

    def save(self):
        with db.auto_commit():
            db.session.add(self)

    @classmethod
    def get(cls, uid):
        return cls.query.filter_by(soft=True, uid=uid).first()
