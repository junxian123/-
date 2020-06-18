from flask import g

from app.libs.enums import PendingStatus
from app.models.drift import Drift
from app.view_models.base import Base


class DriftViewModel(Base):
    _fields = ['id', 'book_title', 'book_id' , 'book_img', 'book_author', 'gift_id',  'gifter_nickname',
               'requester_nickname', 'recipient_name', 'mobile', 'address', 'message', 'pending', 'pending_status',
               'create_time']
    def __init__(self, drift):
        self.id = drift.id
        self.book_id = drift.bid
        self.book_title = drift.book_title
        self.book_img = drift.book_img
        self.book_author = drift.book_author
        self.gift_id = drift.gift_id
        self.gifter_nickname = drift.gifter_nickname
        self.requester_nickname = drift.requester_nickname
        self.recipient_name = drift.recipient_name
        self.mobile = drift.mobile
        self.address = drift.address
        self.message = drift.message
        self.create_time = drift.create_time
        self.pending = self.get_pending(drift.pending, drift.id)
        self.pending_status = drift.pending.value

    @staticmethod
    def get_pending(pending, drift_id):
        who = Drift.is_gifter_or_requester(drift_id)
        return PendingStatus.pending_str(pending, who)

