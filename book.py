class Book:
    id = 0
    name = ''

    def __init__(self, id, name):
        self.id = id
        self.name = name

    def set_name(self, name):
        self.name = name
