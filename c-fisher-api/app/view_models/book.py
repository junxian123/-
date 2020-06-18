

from app.view_models.base import Base


class BookViewModel(Base):
    _fields = ['id', 'title', 'author', 'binding', 'publisher', 'price', 'pages', 'pubdate', 'isbn', 'image']
    def __init__(self, book):
        self.id = book.id
        self.title = book.title
        self.author = book.author
        self.binding = book.binding
        self.publisher = book.publisher
        self.price = book.price
        self.pages = book.pages
        self.pubdate = book.pubdate
        self.isbn = book.isbn
        self.image = book.image