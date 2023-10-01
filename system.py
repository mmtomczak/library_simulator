from book import Book
from person import Worker, Customer
import datetime

WORKER_ID_TYPE = "110"
BOOK_ID_TYPE = "220"
CUSTOMER_ID_TYPE = "330"

# TODO: position-specific roles for worker functionality


class LibrarySystem:
    """Creates object of LibrarySystem class

    Attributes:
        _books (list of Book): List of all books in the library
        _workers (list of Worker): List of all workers in the library
        _customers (list of Customer): List of all customers of the library
        _new_book_id (int): Next in line id number for new book
        _new_worker_id (int): Next in line id number for new worker
        _new_customer_id (int): Next in line id number for new customer
    """
    def __init__(self):
        self._books = []
        self._workers = []
        self._customers = []
        self._new_book_id = int(BOOK_ID_TYPE + '0')  # next in line ID number for book
        self._new_worker_id = int(WORKER_ID_TYPE + '0')  # next in line ID number for worker
        self._new_customer_id = int(CUSTOMER_ID_TYPE + '0')  # next in line ID number for customer
        self.date = datetime.datetime.now()

    @property
    def books(self):
        """list of Book: Returns list of all books in the library"""
        return self._books

    @property
    def workers(self):
        """list of Worker: Returns list of all workers in the library"""
        return self._workers

    @property
    def customers(self):
        """list of Customer: Returns list of all customers of the library"""
        return self._customers

    def add_book(self, title: str, author: str, iban=None, publisher=None, year_published=None):
        """
        Adds new book to the library book list.

        Args:
            title (str): Title of the book
            author (str): Author of the book
            iban (str, optional): Book's IBAN number
            publisher (str, optional): publisher of the book
            year_published (int, optional): Year of the book publication

        """
        self._books.append(Book(title=title,
                                author=author,
                                id=self.return_and_update_id(self._new_book_id),
                                iban=iban,
                                publisher=publisher,
                                year_published=year_published))

    def add_worker(self, name: str, position: str):
        """
        Adds library worker.

        Args:
            name (str): Name of the worker
            position (str): Position of the worker
        """
        self._workers.append(Worker(name=name,
                                    id=self.return_and_update_id(self._new_worker_id),
                                    position=position))

    def add_customer(self, name: str):
        """
        Adds library customer.

        Args:
            name (str): Name of the customer
        """
        self._customers.append(Customer(name=name,
                                        id=self.return_and_update_id(self._new_customer_id)))

    def remove_book(self, book_id: int):
        """
        Removes book from the library.

        Args:
            book_id (int): ID of the book

        Returns:
            True if successful, else False
        """
        for book in self._books:
            if book.id == book_id:
                self._books.remove(book)
                return True
        return False

    def remove_worker(self, worker_id: int):
        """
        Removes worker from the library

        Args:
            worker_id (int): ID of the worker

        Returns:
            True if successful, else False
        """
        for worker in self._workers:
            if worker.id == worker_id:
                self._workers.remove(worker)
                return True
        return False

    def remove_customer(self, customer_id: int):
        """
        Removes customer from the library

        Args:
            customer_id (int): ID of the customer

        Returns:
            True if successful, else False
        """
        for customer in self._customers:
            if customer.id == customer_id:
                self._customers.remove(customer)
                return True
        return False

    def return_and_update_id(self, id: int):
        """
        Returns provided ID number that is next in line in system to be assigned and
        updates ID of provided stored in system type.

        Args:
            id (int): ID to be returned and updated

        Returns:
            Provided ID
        """
        # Function role is to update ID of given type at the time of the ID assigment
        id = str(id)
        # Create new next in line ID
        new_id = int(id[:3] + str(int(id[3:]) + 1))
        # Update ID in the system
        self.update_id(new_id)
        return int(id)

    def update_id(self, new_id: int):
        """
        Updates nex in line ID of given type stored in the system.

        Args:
            new_id (int): New ID to be stored in the system
        """
        # Get the ID type
        id_type = str(new_id)[:3]
        if id_type == WORKER_ID_TYPE:
            self._new_worker_id = new_id
        elif id_type == BOOK_ID_TYPE:
            self._new_book_id = new_id
        elif id_type == CUSTOMER_ID_TYPE:
            self._new_customer_id = new_id
        else:
            # If provided ID has type not recognized in the system raise error
            raise ValueError("Incorrect ID type value")

    @staticmethod
    def reset_id(item_list: list):
        """
        Resets the ID's of objects in the item_list. Objects in the list must have ID attribute.

        Args:
            item_list (list):

        Returns:
            True if successful, else False
        """
        if len(item_list) == 0:
            return False

        id_type = str(item_list[0].id)[:3]

        for number, item in enumerate(item_list):
            item.id = int(id_type + str(number))
        return True

    def rent_book(self, customer_id: int, book_id: int):
        """
        Rents a book to a customer.

        Args:
            customer_id (int): ID of a customer that rents the book
            book_id (int): ID of the rented book

        Returns:
            True if successful, False otherwise
        """
        book = self.get_book_by_id(book_id)
        customer = self.get_customer_by_id(customer_id)
        # If book queue isn't empty it cannot be rented
        if book.queue:
            return False
        # Customer can't rent two the same books
        if book in customer.rented_books:
            return False

        return_time = self.date + datetime.timedelta(days=30)
        book.rent_book(customer, return_time)
        customer.rent_book(book)
        return True

    def add_to_queue(self, customer_id: int, book_id: int):
        """
        Adds customer to the book waiting queue.

        Args:
            customer_id (int): ID of a customer that is to be added to queue
            book_id (int): ID of book that queue is updated

        Returns:
            True if successful, else False
        """
        book = self.get_book_by_id(book_id)
        customer = self.get_customer_by_id(customer_id)
        if Customer in book.queue:
            # If customer is already in the queue return False
            return False

        book.add_to_queue(customer)
        return True

    def remove_from_queue(self, customer_id: int, book_id: int):
        """
        Removes customer from book queue (if present in queue)

        Args:
            customer_id (int): ID of a customer that is to be removed from book queue
            book_id (int): ID of a book from whose queue customer is to be remover

        Returns:
            True if successful, False otherwise
        """
        customer = self.get_customer_by_id(customer_id)
        book = self.get_book_by_id(book_id)

        if customer in book.queue:
            book.queue.remove(customer)
            return True
        return False

    def return_book(self, customer_id: int, book_id: int) -> float:
        """
        Returns rented book to the library.

        Args:
            customer_id (int): ID of a customer
            book_id (int): ID of a book

        Returns:
            float: Fee value to be paid for late return
        """
        book = self.get_book_by_id(book_id)
        customer = self.get_customer_by_id(customer_id)
        # if provided book is not rented by provided customer raise ValueError
        if book not in customer.rented_books:
            raise ValueError
        fee = self.calculate_fee(book)
        customer.return_book(book)
        book.return_book()
        return fee

    def is_book_rented(self, book_id: int):
        """
        Returns information about book's current rent status

        Args:
            book_id (int): ID of book

        Returns:
            True if book is rented, False otherwise
        """
        book = self.get_book_by_id(book_id)
        return book.is_rented()

    def get_book_due_date(self, book_id: int):
        """
        Returns book's return date

        Args:
            book_id: ID of a book

        Returns:
            Return date if book is rented, 0 otherwise
        """
        if not self.is_book_rented(book_id):
            return 0
        book = self.get_book_by_id(book_id)
        return book.return_date

    def get_book_by_id(self, id: int):
        """
        Returns Book class instance of a given ID

        Args:
            id (int): ID of a book

        Returns:
            Book class instance if found ID match, None otherwise
        """
        for book in self._books:
            if book.id == id:
                return book
        return None

    def get_customer_by_id(self, id: int):
        """
        Returns Customer class instance of a given ID

        Args:
            id (int): ID of a customer

        Returns:
            Customer class instance if found ID match, None otherwise
        """
        for customer in self._customers:
            if customer.id == id:
                return customer
        return None

    def get_worker_by_id(self, id: int):
        """
        Returns Worker class instance of a given ID

        Args:
            id (int): ID of a worker

        Returns:
            Worker class instance if found ID match, None otherwise
        """
        for worker in self._workers:
            if worker.id == id:
                return worker
        return None

    def calculate_fee(self, book: Book):
        #
        """
        Calculates fee that is due for the book that is being returned to the library.

        Args:
            book (Book): Book that is being returned to the library

        Returns:
            float: 0.0 if return date is before book due date, else fee amount
        """
        if book.return_date > self.date:
            return 0.0
        else:
            delta = self.date - book.return_date
            return delta.days * 0.5

    def update_date(self, delta=None):
        """
        Updates library date attribute. When delta is None date is being updated to current date.

        Args:
            delta (optional): Amount of days that are to be added to the current library date
        """
        if delta:
            self.date = self.date + datetime.timedelta(days=delta)
        else:
            self.date = datetime.datetime.now()
