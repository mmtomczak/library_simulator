
class Person:
    """
    Class representing a person

    Args:
        name: Name of the person
        id: ID of the person
    """
    def __init__(self, name, id):
        self._name = name
        self._id = id

    @property
    def name(self):
        """Getter and setter of name"""
        return self._name

    @property
    def id(self):
        """Getter and setter of ID"""
        return self._id

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @id.setter
    def id(self, new_id):
        self._id = new_id


class Worker(Person):
    """
    Class representing a Worker

    Args:
        name: Name of the worker
        id: ID of the worker
        position: Position of the worker
    """
    def __init__(self, name, id, position):
        super().__init__(name, id)
        self._position = position

    @property
    def position(self):
        """Getter and setter of the position"""
        return self._position

    @position.setter
    def position(self, new_position):
        self._position = new_position


class Customer(Person):
    """
    Class representing a Customer

    Args:
        name: Name of the customer
        id: ID of the customer

    Attributes:
        rented_books(list): List of books rented by the customer
        rating(int): Rating of the customer
    """
    def __init__(self, name, id):
        super().__init__(name, id)
        self.rented_books = []
        self.rating = 0

    def return_book(self, book):
        """
        Removes a book from customer's list of rented books

        Args:
            book: Book to be deleted
        """
        self.rented_books.remove(book)

    def rent_book(self, book):
        """
        Adds book to customer's rented books list

        Args:
            book: Book to be added to list
        """
        self.rented_books.append(book)
