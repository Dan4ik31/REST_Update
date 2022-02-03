from src.book import Book


class Subject:
    id = 0
    name = ''
    book = []
    def __init__(self, id):
        self.id = id

    def add_book(self, book: Book):
        self.book.insert(book)
