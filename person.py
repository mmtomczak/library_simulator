
class Person:
    def __init__(self, name, id):
        self._name = name
        self._id = id

    @property
    def name(self):
        return self._name

    @property
    def id(self):
        return self._id

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @id.setter
    def id(self, new_id):
        self._id = new_id


class Worker(Person):
    def __init__(self, name: str, id, position):
        super().__init__(name, id)
        self._position = position

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position


class Customer(Person):
    def __init__(self, name, id):
        super().__init__(name, id)
        self.rented_books = []
        self.rating = 0

    def return_book(self, book):
        self.rented_books.remove(book)

    def rent_book(self, book):
        self.rented_books.append(book)
        return True


