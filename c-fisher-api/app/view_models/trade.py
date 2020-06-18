from flask import g
from lin.db import MixinJSONSerializer


from app.models.drift import Drift
from app.view_models.base import Base
from app.view_models.book import BookViewModel


class BookDetailViewModel(MixinJSONSerializer):
    _fields = ['is_gifter', 'is_wisher', 'book', 'gifted', 'wished']

    def __init__(self, is_gifter=False, is_wisher=False, book=None, gifts=None, wishes=None):
        self.is_gifter = is_gifter
        self.is_wisher = is_wisher
        self.book = book
        self.gifted = TradeInfo(gifts, self.is_gifter, self.is_wisher)
        self.wished = TradeInfo(wishes, self.is_gifter, self.is_wisher)


class Trade(Base):
    _fields = ['id', 'create_time', 'nickname', 'is_gifted_or_requested']
    def __init__(self, trade, is_gifter=False, is_wisher=False):
        self.is_gifter = is_gifter
        self.is_wisher = is_wisher
        self.trade = trade

        self.id = trade.id
        self.create_time = trade.create_time
        self.nickname = trade.consumer.wx_name

        self.gifter_id = self.__get_gifter_id()
        self.request_id = self.__get_request_id()
        self.is_gifted_or_requested = Drift.is_gifted_or_requested(trade.bid, self.gifter_id, self.request_id)

    def __get_gifter_id(self):
        uid = g.user.id
        if self.is_gifter:
            return uid
        return self.trade.consumer.id

    def __get_request_id(self):
        uid = g.user.id
        if self.is_wisher:
            return uid
        return self.trade.consumer.id

class TradeInfo(Base):
    _fields = ['total', 'trades']

    def __init__(self, trades, is_gifter=False, is_wisher=False):
        self.total = len(trades)
        self.trades = [Trade(trade, is_gifter, is_wisher) for trade in trades]

class MyTrade(Base):
    _fields = ['trades', 'total']
    def __init__(self, trades_of_mine, trades_count_list):
        self.total = len(trades_of_mine)
        self.__trades_of_mine = trades_of_mine
        self.__trades_count_list = trades_count_list
        self.trades = self.__parse()

    def __parse(self):
        trades = []
        books = [BookViewModel(trade.book) for trade in self.__trades_of_mine]
        for book in books:
            trade = self.__maching(book)
            trades.append(trade)
        return trades

    def __maching(self, book):
        count = 0
        for trade_count in self.__trades_count_list:
            if trade_count.bid == book.id:
                count = trade_count.count
                break
        return {
            'book': book,
            'count': count
        }