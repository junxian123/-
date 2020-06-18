"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from lin.exception import NotFound, ParameterException
from sqlalchemy import Column, String, Integer
from lin.interface import InfoCrud as Base
from app.libs.error_code import BookNotFound


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(200), default='未名')
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=True, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))

    @classmethod
    def get_book_by_isbn(cls, isbn):
        book = cls.query.filter_by(isbn=isbn, soft=True).first()
        if book is None:
            raise BookNotFound()
        return book

    @classmethod
    def search_by_keywords(cls, q):
        books = cls.query.filter(Book.title.like('%' + q + '%')).all()
        if not books:
            raise BookNotFound()
        return books


    @classmethod
    def get_detail(cls, bid):
        book = cls.query.filter_by(id=bid, soft=True).first()
        if book is None:
            raise NotFound(msg='没有找到相关书籍')
        return book

    @classmethod
    def get_all(cls):
        books = cls.query.filter_by().all()
        cls.get()
        if not books:
            raise NotFound(msg='没有找到相关书籍')
        return books

    @classmethod
    def new_book(cls, form):
        book = Book.query.filter_by(title=form.title.data).first()
        if book is not None:
            raise ParameterException(msg='图书已存在')

        Book.create(
            title=form.title.data,
            author=form.author.data,
            summary=form.summary.data,
            image=form.image.data,
            commit=True
        )
        return True

    @classmethod
    def edit_book(cls, bid, form):
        book = Book.query.filter_by(id=bid).first()
        if book is None:
            raise NotFound(msg='没有找到相关书籍')

        book.update(
            id=bid,
            title=form.title.data,
            author=form.author.data,
            summary=form.summary.data,
            image=form.image.data,
            commit=True
        )
        return True

    @classmethod
    def remove_book(cls, bid):
        book = cls.query.filter_by(id=bid).first()
        if book is None:
            raise NotFound(msg='没有找到相关书籍')
        # 删除图书，软删除
        book.delete(commit=True)
        return True
