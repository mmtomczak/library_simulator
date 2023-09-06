

class Book:
    def __init__(self, title, author, id, iban, publisher, year_published):
        self._title = title
        self._author = author
        self._iban = iban
        self._id = id
        self._publisher = publisher
        self._year_published = year_published
        self.current_renter = None
        self.return_date = None
        self.queue = []

    def rent_book(self, renter, return_time):
        self.current_renter = renter
        self.return_date = return_time

    def return_book(self):
        self.current_renter = None
        self.return_date = None

    def is_rented(self):
        if self.current_renter is None:
            return False

        return True

    def add_to_queue(self, person):
        if person in self.queue:
            return False

        self.queue.append(person)
        return True

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def iban(self):
        return self._iban

    @property
    def id(self):
        return self._id

    @property
    def publisher(self):
        return self._publisher

    @property
    def year_published(self):
        return self._year_published

    @title.setter
    def title(self, new_title):
        self._title = new_title

    @author.setter
    def author(self, new_author):
        self._author = new_author

    @iban.setter
    def iban(self, new_iban: str):
        self._iban = new_iban

    @id.setter
    def id(self, new_id):
        self._id = new_id

    @publisher.setter
    def publisher(self, new_publisher):
        self._publisher = new_publisher

    @year_published.setter
    def year_published(self, new_year):
        self._year_published = new_year
