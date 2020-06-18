
from lin.interface import InfoCrud

class Base(InfoCrud):

    __abstract__ = True

    @classmethod
    def paged_query(cls, start=None, pre_page_count=None, **kwargs):
        # 分页查询--1 不会出现重复图书记录；2 时间排序
        if kwargs.get('delete_time') is None:
            kwargs['delete_time'] = None

        return cls.query.filter_by(**kwargs).order_by(
            '-create_time').group_by(cls.bid).distinct().offset(start).limit(pre_page_count).all()

    @classmethod
    def get_total(cls, **kwargs):
        # 获取总记录数--1 不会出现重复图书记录；
        if kwargs.get('delete_time') is None:
            kwargs['delete_time'] = None

        return cls.query.filter_by(**kwargs).group_by(cls.bid).distinct().count()

