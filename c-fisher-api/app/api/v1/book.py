"""
    a standard CRUD template of book
    通过 图书 来实现一套标准的 CRUD 功能，供学习
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""
from flask import jsonify, g
from lin import route_meta, group_required, login_required
from lin.exception import Success
from lin.log import Logger
from lin.redprint import Redprint

from app.libs.token_auth import auth
from app.libs.utils import is_isbn_or_key
from app.models.book import Book
from app.models.gift import Gift
from app.models.wish import Wish
from app.validators.forms import BookSearchForm, CreateOrUpdateBookForm
from app.view_models.book import BookViewModel
from app.view_models.trade import BookDetailViewModel

book_api = Redprint('book')

@book_api.route('/detail/<int:bid>', methods=['GET'])
@auth.login_required
def get_book_detail(bid):
    uid = g.user.id
    is_wisher = False
    is_gifter = Gift.is_gifter(bid, uid)
    if not is_gifter:
        is_wisher = Wish.is_wisher(bid, uid)

    book = Book.get_detail(bid)
    gifts = Gift.get_gifts_by_bid(bid)
    wishes = Wish.get_wishes_by_bid(bid)

    book_detail = BookDetailViewModel(is_gifter, is_wisher, book, gifts, wishes)
    return jsonify(book_detail), 200


@book_api.route('/<q>/<count>/<start>')
def save(q, count, start):
    Book.reptile(q, count, start)
    return Success()


@book_api.route('/<int:bid>', methods=['get'])
def get_book(bid):
    book = Book.query.get(bid)
    return jsonify(BookViewModel(book)), 200


@book_api.route('/', methods=['GET'])
@login_required
@Logger(template='{user.nickname}查询了所有图书')
def get_books():
    books = Book.get_all()
    return jsonify(books)

@book_api.route('/search', methods=['POST'])
def search():
    form = BookSearchForm().validate_for_api()
    q = form.q.data
    if is_isbn_or_key(q) == 'key':
        books = Book.search_by_keywords(q)
    else:
        books = [Book.get_book_by_isbn(q)]
    return jsonify(books), 200

@book_api.route('/', methods=['POST'])
def create_book():
    form = CreateOrUpdateBookForm().validate_for_api()
    Book.new_book(form)
    return Success(msg='新建图书成功')


@book_api.route('/<bid>', methods=['PUT'])
def update_book(bid):
    form = CreateOrUpdateBookForm().validate_for_api()
    Book.edit_book(bid, form)
    return Success(msg='更新图书成功')


@book_api.route('/<bid>', methods=['DELETE'])
@route_meta(auth='删除图书', module='图书')
@group_required
def delete_book(bid):
    Book.remove_book(bid)
    return Success(msg='删除图书成功')
