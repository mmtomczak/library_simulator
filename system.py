from book import Book
from person import Worker, Customer
import datetime

WORKER_ID_TYPE = "110"
BOOK_ID_TYPE = "220"
CUSTOMER_ID_TYPE = "330"


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
        self._new_book_id = int(BOOK_ID_TYPE + '0')
        self._new_worker_id = int(WORKER_ID_TYPE + '0')
        self._new_customer_id = int(CUSTOMER_ID_TYPE + '0')
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
        """Adds new book to the library book list

        Args:
            title (str): Title of the book
            author (str): Author of the book
            iban (str): book's IBAN number
            publisher (str): publisher of the book
            year_published (int): Year of the book publication

        """
        self._books.append(Book(title=title,
                                author=author,
                                id=self.return_and_update_id(self._new_book_id),
                                iban=iban,
                                publisher=publisher,
                                year_published=year_published))

    def add_worker(self, name: str, position: str):
        self._workers.append(Worker(name=name,
                                    id=self.return_and_update_id(self._new_worker_id),
                                    position=position))

    def add_customer(self, name: str):
        self._customers.append(Customer(name=name,
                                        id=self.return_and_update_id(self._new_customer_id)))

    def remove_book(self, book_id: int):
        for book in self._books:
            if book.id == book_id:
                self._books.remove(book)
                return True

        return False

    def remove_worker(self, worker_id: int):
        for worker in self._workers:
            if worker.id == worker_id:
                self._workers.remove(worker)
                return True

        return False

    def remove_customer(self, customer_id: int):
        for customer in self._customers:
            if customer.id == customer_id:
                self._customers.remove(customer)
                return True

        return False

    def return_and_update_id(self, id: int):
        id = str(id)
        new_id = int(id[:3] + str(int(id[3:]) + 1))
        self.update_id(new_id)
        return int(id)

    def update_id(self, new_id: int):
        id_type = str(new_id)[:3]
        if id_type == WORKER_ID_TYPE:
            self._new_worker_id = new_id
        elif id_type == BOOK_ID_TYPE:
            self._new_book_id = new_id
        elif id_type == CUSTOMER_ID_TYPE:
            self._new_customer_id = new_id
        else:
            raise ValueError("Incorrect ID type value")

    @staticmethod
    def reset_id(item_list: list):
        if len(item_list) == 0:
            return False

        id_type = str(item_list[0].id)[:3]

        for number, item in enumerate(item_list):
            item.id = int(id_type + str(number))

        return True

    def try_rent_book(self, customer: Customer, book_id: int):
        book = self.get_book_by_id(book_id)
        if book.queue:
            book.add_to_queue(customer)
            return False

        return_time = self.date + datetime.timedelta(days=30)
        book.rent_book(customer, return_time)
        customer.rent_book(book)
        return True

    def return_book(self, customer: Customer, book_id: int):
        book = self.get_book_by_id(book_id)
        fee = self.calculate_fee(book)

        customer.return_book(book)
        book.return_book()
        return fee

    def get_book_by_id(self, id: int):
        for book in self._books:
            if book.id == id:
                return book

        return None

    def calculate_fee(self, book: Book):
        if book.return_date > self.date:
            return 0

        else:
            delta = self.date - book.return_date
            return delta.days * 0.5

    def update_date(self, delta=None):
        if delta:
            self.date = self.date + datetime.timedelta(days=delta)
        else:
            self.date = datetime.datetime.now()
