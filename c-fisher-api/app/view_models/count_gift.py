from app.view_models.base import Base
class CountGift(Base):
    _fields = ['time', 'count']
    def __init__(self, data):
        self.time = data[0]
        self.count = data[1]