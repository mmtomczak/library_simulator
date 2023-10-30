import datetime
import sqlite3
import pytest
from system import LibrarySystem
from database_generator import DatabaseGenerator

TEST_DB_PATH = "database/test.db"

TEST_DATASET = {
    "books_data": [
            (2200, "book1", "author1", "isbn1", "publisher", 1990),
            (2201, "book2", "author2", "isbn2", "publisher", 1990),
            (2202, "book3", "author3", "isbn3", "publisher", 1990),
        ],
    "customers_data": [
            (3300, "customer1"),
            (3301, "customer2"),
            (3302, "customer3"),
        ],
    "workers_data": [
            (1100, "worker1", "position"),
            (1101, "worker2", "position"),
        ],
    "queues": [
            (3300, 2200),
            (3300, 2201),
            (3301, 2201),
            (3302, 2201)
        ],
    "rents": [
            (2200, 3301, datetime.datetime.now() + datetime.timedelta(30)),
            (2202, 3302, datetime.datetime.now() + datetime.timedelta(1))
        ]
}


@pytest.fixture
def library_simple():
    sys = LibrarySystem()
    sys.add_book("title", "author", "isbn", "publisher", 2000)
    sys.add_worker("worker", "position")
    sys.add_customer("customer")
    return sys


@pytest.fixture
def library_database():
    DatabaseGenerator(TEST_DB_PATH, test_db=True, dataset=TEST_DATASET)
    sys = LibrarySystem(database=TEST_DB_PATH)
    sys.load_database()
    return sys

# NO DATABASE LIBRARY TESTS


def test_add_book(library_simple):
    library_simple.add_book("title", "author", "isbn", "publisher", 2000)
    assert len(library_simple.books) == 2 and library_simple.books[1].title == "title"


def test_add_worker(library_simple):
    library_simple.add_worker("worker", "position")
    assert len(library_simple.workers) == 2 and library_simple.workers[1].name == "worker"


def test_add_customer(library_simple):
    library_simple.add_customer("customer")
    assert len(library_simple.customers) == 2 and library_simple.customers[0].name == "customer"


def test_remove_book(library_simple):
    library_simple.remove_book(0)
    assert len(library_simple.books) == 0


def test_remove_worker(library_simple):
    library_simple.remove_worker(0)
    assert len(library_simple.workers) == 0


def test_remove_customer(library_simple):
    library_simple.remove_customer(0)
    assert len(library_simple.customers) == 0


def test_return_and_update_id_book(library_simple):
    result = library_simple.return_and_update_id(4, "_new_book_id")
    assert result == 4 and library_simple._new_book_id == 5


def test_return_and_update_id_worker(library_simple):
    result = library_simple.return_and_update_id(4, "_new_worker_id")
    assert result == 4 and library_simple._new_worker_id == 5


def test_return_and_update_id_customer(library_simple):
    result = library_simple.return_and_update_id(4, "_new_customer_id")
    assert result == 4 and library_simple._new_customer_id == 5


def test_rent_book_no_queue(library_simple):
    result = library_simple.rent_book(0, 0)
    assert result and library_simple.is_book_rented(0)


def test_rent_book_first_in_queue(library_simple):
    queue_result = library_simple.add_to_queue(0, 0)
    rent_result = library_simple.rent_book(0, 0)
    assert queue_result and rent_result and library_simple.is_book_rented(0)


def test_rent_book_in_queue(library_simple):
    library_simple.add_customer("customer")
    queue_result = library_simple.add_to_queue(1, 0)
    rent_result = library_simple.rent_book(0, 0)
    assert queue_result and not rent_result and not library_simple.is_book_rented(0)


def test_add_to_queue(library_simple):
    result = library_simple.add_to_queue(0, 0)
    assert result and len(library_simple.books[0].queue) == 1


def test_remove_from_queue(library_simple):
    library_simple.add_to_queue(0, 0)
    result = library_simple.remove_from_queue(0, 0)
    assert result and len(library_simple.books[0].queue) == 0


def test_try_remove_from_queue(library_simple):
    result = library_simple.remove_from_queue(0, 0)
    assert not result and len(library_simple.books[0].queue) == 0


def test_return_book(library_simple):
    library_simple.rent_book(0, 0)
    library_simple.return_book(0, 0)
    assert not library_simple.is_book_rented(0)


def test_is_book_rented(library_simple):
    assert not library_simple.is_book_rented(0)


def test_get_book_due_date(library_simple):
    library_simple.rent_book(0, 0)
    assert type(library_simple.books[0].return_date) == datetime.datetime


def test_get_book_by_id(library_simple):
    book = library_simple.get_book_by_id(0)
    assert book.title == "title" and book.author == "author"


def test_get_customer_by_id(library_simple):
    customer = library_simple.get_customer_by_id(0)
    assert customer.name == "customer"


def test_get_worker_by_id(library_simple):
    worker = library_simple.get_worker_by_id(0)
    assert worker.name == "worker" and worker.position == "position"


def test_calculate_fee(library_simple):
    library_simple.rent_book(0, 0)
    library_simple.update_date(50)
    result = library_simple.return_book(0, 0)
    assert type(result) == float and result == 20 * 0.5


def test_update_date(library_simple):
    now = datetime.datetime.now()
    library_simple.update_date(1)
    tomorrow = now + datetime.timedelta(days=1)
    assert library_simple.date.day == tomorrow.day


def test_set_ids(library_simple):
    library_simple._set_ids()
    assert library_simple._new_book_id == 1 and library_simple._new_worker_id == 1 \
           and library_simple._new_customer_id == 1


def test_load_database(library_simple):
    result = library_simple.load_database()
    assert not result


# DATABASE LIBRARY TESTS


def test_load_test_db(library_database):
    assert library_database.books and library_database.customers and library_database.workers


def test_books_db(library_database):
    assert (library_database.books[0].title == TEST_DATASET["books_data"][0][1]
            and len(library_database.books) == len(TEST_DATASET["books_data"]))


def test_ids_updates(library_database):
    assert (library_database._new_book_id == TEST_DATASET["books_data"][-1][0] + 1
            and library_database._new_customer_id == TEST_DATASET["customers_data"][-1][0] + 1
            and library_database._new_worker_id == TEST_DATASET["workers_data"][-1][0] + 1)


def test_workers_db(library_database):
    assert (library_database.workers[0].name == TEST_DATASET["workers_data"][0][1]
            and len(library_database.workers) == len(TEST_DATASET["workers_data"]))


def test_customers_db(library_database):
    assert (library_database.customers[0].name == TEST_DATASET["customers_data"][0][1]
            and len(library_database.customers) == len(TEST_DATASET["customers_data"]))


def test_close_database_db(library_database):
    library_database._close_database()
    with pytest.raises(sqlite3.ProgrammingError) as err:
        library_database._cursor.execute("SELECT * FROM books")


def test_add_book_db(library_database):
    library_database.add_book(title="titlex", author="authorx", isbn="isbnx", publisher="publisher", year_published=999)
    assert ((len(library_database.books) == len(TEST_DATASET["books_data"]) + 1
            and library_database._cursor.execute("SELECT * FROM books")).fetchall()[-1][0:2]
            == (library_database._new_book_id - 1, "titlex"))


def test_add_worker_db(library_database):
    library_database.add_worker(name="workerx", position="position")
    assert ((len(library_database.workers) == len(TEST_DATASET["workers_data"]) + 1
            and library_database._cursor.execute("SELECT * FROM workers")).fetchall()[-1][0:2]
            == (library_database._new_worker_id - 1, "workerx"))


def test_add_customer_db(library_database):
    library_database.add_customer(name="customerx")
    assert ((len(library_database.customers) == len(TEST_DATASET["customers_data"]) + 1
            and library_database._cursor.execute("SELECT * FROM customers")).fetchall()[-1][0:2]
            == (library_database._new_customer_id - 1, "customerx"))


def test_remove_book_db(library_database):
    library_database.remove_book(book_id=TEST_DATASET["books_data"][0][0])
    assert (len(library_database.books) == len(TEST_DATASET["books_data"]) - 1
            and library_database._cursor.execute("SELECT * FROM books").fetchall()[0] == TEST_DATASET["books_data"][1])


def test_remove_worker_db(library_database):
    library_database.remove_worker(worker_id=TEST_DATASET["workers_data"][0][0])
    assert (len(library_database.workers) == len(TEST_DATASET["workers_data"]) - 1 and
            library_database._cursor.execute("SELECT * FROM workers").fetchall()[0] == TEST_DATASET["workers_data"][1])


def test_remove_customer_db(library_database):
    library_database.remove_customer(customer_id=TEST_DATASET["customers_data"][0][0])
    assert (len(library_database.customers) == len(TEST_DATASET["customers_data"]) - 1 and
            library_database._cursor.execute("SELECT * FROM customers").fetchall()[0] == TEST_DATASET["customers_data"][1])


def test_rent_book_db():
    pass


def test_add_to_queue_db():
    pass


def test_remove_from_queue_db():
    pass


def test_return_book_db():
    pass


def test_is_book_rented_db():
    pass


def test_get_book_due_date_db():
    pass


def test_get_book_by_id_db():
    pass


def test_get_customer_by_id_db():
    pass


def test_get_worker_by_id_db():
    pass


def test_calculate_fee_db():
    pass


def test_update_date_db():
    pass


def test_set_ids_db():
    pass


def test_load_database_db():
    pass