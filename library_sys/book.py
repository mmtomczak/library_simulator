
class Book:
    """
    Creates object of Book class

    Args:
        title: Title of the book
        author: Author of the book
        isbn: ISBN of the book
        publisher: Publisher of the book
        year_published: Year of the book publication
        id: ID of the book

    Attributes:
        current_renter: Current book renter
        return_date: Book return date
        queue: Book rent queue
    """
    def __init__(self, title, author, id, isbn, publisher, year_published):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._id = id
        self._publisher = publisher
        self._year_published = year_published
        self.current_renter = None
        self.return_date = None
        self.queue = []

    def rent_book(self, renter, return_time):
        """
        Rents the book to the given renter

        Args:
            renter: Renter of the book
            return_time: Return time of the book
        """
        self.current_renter = renter
        self.return_date = return_time

    def return_book(self):
        """
        Returns the book
        """
        self.current_renter = None
        self.return_date = None

    def is_rented(self):
        """
        Checks if book is rented

        Returns:
            True if rented, False otherwise
        """
        if self.current_renter is None:
            return False
        return True

    def add_to_queue(self, person):
        """
        Adds person to the book's rent queue

        Args:
            person: Person that is to be added to queue
        """
        self.queue.append(person)

    @property
    def title(self):
        """Get or set book title"""
        return self._title

    @property
    def author(self):
        """Get or set book author"""
        return self._author

    @property
    def isbn(self):
        """Get or set book ISBN"""
        return self._isbn

    @property
    def id(self):
        """Get or set book ID"""
        return self._id

    @property
    def publisher(self):
        """Get or set book publisher"""
        return self._publisher

    @property
    def year_published(self):
        """Get or set book publication year"""
        return self._year_published

    @title.setter
    def title(self, new_title):
        self._title = new_title

    @author.setter
    def author(self, new_author):
        self._author = new_author

    @isbn.setter
    def isbn(self, new_isbn):
        self._isbn = new_isbn

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @publisher.setter
    def publisher(self, new_publisher):
        self._publisher = new_publisher

    @year_published.setter
    def year_published(self, new_year):
        self._year_published = new_year
