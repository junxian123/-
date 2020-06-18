import requests

"""
    create by xian on 2019/4/16
"""
import requests

import lin.interface as Base

class Book():
    def __init__(self,book):
        self.id = book['id']
        self.title = book['title']
        self.author = book['author']
        self.binding = book['binding']
        self.publisher = book['publisher']
        self.price = book['price']
        self.pages = book['pages']
        self.pubdate = book['pubdate']
        self.isbn = book['isbn']
        self.image = book['image']
        self.summary = book['summary']


class YuShuBook:
    isbn_url = 'http://t.yushu.im/v2/book/isbn/{}'
    key_url = 'http://t.yushu.im/v2/book/search?q={}&count={}&start={}'

    def __init__(self):
        self.books = []

    def parse(self):
        self.key_url = self.key_url.format('JAVA', 20, 0)
        http = requests.get(self.key_url)
        json = http.json()
        self.books = [Book(j)for j in json['books']]


yuShuBook = YuShuBook()
yuShuBook.parse()