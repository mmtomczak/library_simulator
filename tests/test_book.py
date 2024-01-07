import pytest

from library_sys.book import Book

SAMPLE_BOOK = {"title": "book tests",
               "author": "boo author",
               "id": 111,
               "isbn": "isbn123",
               "publisher": "book publisher",
               "year_published": 2000}


@pytest.fixture
def book():
    return Book(**SAMPLE_BOOK)


def test_rent_book(book):
    book.rent_book("renter", "10-10-2000")
    assert (book.current_renter == "renter") & (book.return_date == "10-10-2000")


def test_return_book(book):
    book.rent_book("renter", "10-10-2000")
    book.return_book()
    assert (book.current_renter is None) & (book.return_date is None)


def test_is_rented_true(book):
    book.rent_book("renter", "10-10-2000")
    assert book.is_rented()


def test_is_rented_false(book):
    book.rent_book("renter", "10-10-2000")
    book.return_book()
    assert not book.is_rented()


def test_add_to_queue(book):
    book.add_to_queue("person1")
    book.add_to_queue("person2")
    book.add_to_queue("person3")
    assert book.queue == ["person1", "person2", "person3"]


def test_title_getter(book):
    assert book.title == SAMPLE_BOOK["title"]


def test_title_setter(book):
    book.title = "new title"
    assert book.title == "new title"


def test_author_getter(book):
    assert book.author == SAMPLE_BOOK["author"]


def test_author_setter(book):
    book.author = "new author"
    assert book.author == "new author"


def test_isbn_getter(book):
    assert book.isbn == SAMPLE_BOOK["isbn"]


def test_isbn_setter(book):
    book.isbn = "new isbn"
    assert book.isbn == "new isbn"


def test_id_getter(book):
    assert book.id == SAMPLE_BOOK["id"]


def test_id_setter(book):
    book.id = 444
    assert book.id == 444


def test_publisher_getter(book):
    assert book.publisher == SAMPLE_BOOK["publisher"]


def test_publisher_setter(book):
    book.publisher = "new publisher"
    assert book.publisher == "new publisher"


def test_year_published_getter(book):
    assert book.year_published == SAMPLE_BOOK["year_published"]


def test_year_published_setter(book):
    book.year_published = "20-20-2020"
    assert book.year_published == "20-20-2020"
