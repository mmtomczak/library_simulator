from book import Book
from person import Worker, Customer
import datetime
import sqlite3


class LibrarySystem:
    """Creates object of LibrarySystem class

    Attributes:
        _books (list of Book): List of all books in the library
        _workers (list of Worker): List of all workers in the library
        _customers (list of Customer): List of all customers of the library
        _new_book_id (int): Next in line id number for new book
        _new_worker_id (int): Next in line id number for new worker
        _new_customer_id (int): Next in line id number for new customer
        date (datetime.datetime): Current date in system
        **fee_rate (int, optional): book overtime return fee rate. Defaults to 0.5
    """
    def __init__(self, **kwargs):
        self._books = []
        self._workers = []
        self._customers = []
        self._new_book_id = 0  # next in line ID number for book
        self._new_worker_id = 0  # next in line ID number for worker
        self._new_customer_id = 0  # next in line ID number for customer
        self.date = datetime.datetime.now()

        try:
            self.fee_rate = kwargs["fee_rate"]
        except KeyError:
            self.fee_rate = 0.5
        try:
            self._connect_to_database(kwargs["database"])
        except KeyError:
            self._db_connection = None
            self._cursor = None

    def __del__(self):
        if self._cursor:
            self._close_database()

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

    def _connect_to_database(self, db_path):
        self._db_connection = sqlite3.connect(db_path)
        self._cursor = self._db_connection.cursor()

    def _close_database(self):
        self._db_connection.close()

    def add_book(self, title: str, author: str, isbn=None, publisher=None, year_published=None, book_id: int = None,
                 database_load: bool = False):
        """
        Adds new book to the library book list.

        Args:
            title (str): Title of the book
            author (str): Author of the book
            isbn (str, optional): Book's ISBN
            publisher (str, optional): publisher of the book
            year_published (int, optional): Year of the book publication
            book_id (int, optional): ID of the book - use only if data is loaded from database
            database_load (bool, optional): set to True if data is not to be added to the database

        """
        if book_id is None:
            book_id = getattr(self, "return_and_update_id")(self._new_book_id, "_new_book_id")

        if not database_load:
            if self._cursor:
                query = (book_id, title, author, isbn, publisher, year_published)
                self._cursor.execute(
                    f"INSERT INTO books(book_id, title, author, isbn, publisher, year_published) VALUES{query}"
                )
                self._db_connection.commit()

        self._books.append(Book(title=title,
                                author=author,
                                id=book_id,
                                isbn=isbn,
                                publisher=publisher,
                                year_published=year_published))

    def add_worker(self, name: str, position: str, worker_id: int = None, database_load: bool = False):
        """
        Adds library worker.

        Args:
            name (str): Name of the worker
            position (str): Position of the worker
            worker_id (int, optional): ID of the worker - use only if data is loaded from database
            database_load (bool, optional): set to True if data is not to be added to the database
        """
        if worker_id is None:
            worker_id = getattr(self, "return_and_update_id")(self._new_worker_id, "_new_worker_id")
        if not database_load:
            if self._cursor:
                query = (worker_id, name, position)
                self._cursor.execute(
                    f"INSERT INTO workers(worker_id, name, position) VALUES{query}"
                )
                self._db_connection.commit()

        self._workers.append(Worker(name=name,
                                    id=worker_id,
                                    position=position))

    def add_customer(self, name: str, customer_id: int = None, database_load: bool = False):
        """
        Adds library customer.

        Args:
            name (str): Name of the customer
            customer_id (int, optional): ID of the customer - use only if data is loaded from database
            database_load (bool, optional): set to True if data is not to be added to the database
        """
        if customer_id is None:
            customer_id = getattr(self, "return_and_update_id")(self._new_customer_id, "_new_customer_id")
        if not database_load:
            if self._cursor:
                query = (customer_id, name)
                self._cursor.execute(
                    f"INSERT INTO customers(customer_id, name) VALUES{query}"
                )
                self._db_connection.commit()

        self._customers.append(Customer(name=name,
                                        id=customer_id))

    def remove_book(self, book_id: int):
        """
        Removes book from the library.

        Args:
            book_id (int): ID of the book

        Returns:
            True if successful, else False
        """
        if self._cursor:
            self._cursor.execute(f"DELETE FROM books WHERE book_id={book_id}")
            self._db_connection.commit()

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
        if self._cursor:
            self._cursor.execute(f"DELETE FROM workers WHERE worker_id={worker_id}")
            self._db_connection.commit()

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
        if self._cursor:
            self._cursor.execute(f"DELETE FROM customers WHERE customer_id={customer_id}")
            self._db_connection.commit()

        for customer in self._customers:
            if customer.id == customer_id:
                self._customers.remove(customer)
                return True
        return False

    def return_and_update_id(self, id: int, kind: str):
        # Create new next in line ID
        new_id = id + 1
        # Update ID in the system
        setattr(self, kind, new_id)
        return id

    def rent_book(self, customer_id: int, book_id: int, return_time=None, database_load: bool = False):
        """
        Rents a book to a customer.

        Args:
            customer_id (int): ID of a customer that rents the book
            book_id (int): ID of the rented book
            return_time (optional): book return date, used when data is loaded from database, defaults to None
            database_load (bool, optional): set to True if data is not to be added to the database

        Returns:
            True if successful, False otherwise
        """
        book = self.get_book_by_id(book_id)
        customer = self.get_customer_by_id(customer_id)
        # If book queue isn't empty it cannot be rented
        if book.queue and book.queue[0] != customer:
            return False
        # Customer can't rent two the same books
        if book in customer.rented_books:
            return False

        if not return_time:
            return_time = self.date + datetime.timedelta(days=30)

        if not database_load:
            if self._cursor:
                self._cursor.execute(
                    f"""INSERT INTO rents(book_id, customer_id, return_date) 
                        VALUES({book_id}, {customer_id}, '{return_time}')"""
                )
                self._db_connection.commit()
        book.rent_book(customer, return_time)
        customer.rent_book(book)
        return True

    def add_to_queue(self, customer_id: int, book_id: int, rent_if_empty: bool = True, database_load: bool = False):
        """
        Adds customer to the book waiting queue.

        Args:
            customer_id (int): ID of a customer that is to be added to queue
            book_id (int): ID of book that queue is updated
            rent_if_empty (bool, optional): automatically rents the book if queue is empty
            database_load (bool, optional): set to True if data is not to be added to the database

        Returns:
            True if successful, else False
        """
        book = self.get_book_by_id(book_id)
        customer = self.get_customer_by_id(customer_id)
        if customer in book.queue:
            # If customer is already in the queue return False
            return False

        if rent_if_empty:
            if not book.queue:
                return self.rent_book(customer_id=customer_id, book_id=book_id, database_load=database_load)

        if not database_load:
            if self._cursor:
                self._cursor.execute(
                    f"""INSERT INTO queues(book_id, customer_id) 
                        VALUES({book_id}, {customer_id})"""
                )
                self._db_connection.commit()

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

            if self._cursor:
                self._cursor.execute(
                    f"DELETE FROM queues WHERE customer_id={customer_id} AND book_id={book_id}"
                )
                self._db_connection.commit()

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

        if self._cursor:
            self._cursor.execute(
                f"DELETE FROM rents WHERE customer_id={customer_id} AND book_id={book_id}"
            )
            self._db_connection.commit()

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
            Return date if book is rented, None otherwise
        """
        if not self.is_book_rented(book_id):
            return None
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
            return delta.days * self.fee_rate

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

    def _set_ids(self):
        self._new_book_id = self.books[-1].id + 1
        self._new_worker_id = self.workers[-1].id + 1
        self._new_customer_id = self.customers[-1].id + 1

    def load_database(self, **kwargs):
        if self._cursor is None:
            return False

        result_books = self._cursor.execute("SELECT * FROM books")
        for row in result_books:
            self.add_book(book_id=row[0], title=row[1], author=row[2], isbn=row[3], publisher=row[4],
                          year_published=row[5], database_load=True)

        result_workers = self._cursor.execute("SELECT * FROM workers")
        for row in result_workers:
            self.add_worker(worker_id=row[0], name=row[1], position=row[2], database_load=True)

        result_customers = self._cursor.execute("SELECT * FROM customers")
        for row in result_customers:
            self.add_customer(customer_id=row[0], name=row[1], database_load=True)

        result_rents = self._cursor.execute("SELECT * FROM rents")
        for row in result_rents:
            self.rent_book(customer_id=row[2], book_id=row[1],
                           return_time=datetime.datetime.strptime(row[3], "%Y-%m-%d %H:%M:%S.%f"),
                           database_load=True)

        result_queues = self._cursor.execute("SELECT * FROM queues")

        try:
            rent_if_empty = kwargs["rent_if_empty"]
        except KeyError:
            rent_if_empty = False

        for row in result_queues:
            self.add_to_queue(customer_id=row[2], book_id=row[1], rent_if_empty=rent_if_empty, database_load=True)

        self._set_ids()
        return True
