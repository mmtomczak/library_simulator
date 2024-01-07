import datetime
import sqlite3
import pytest
from library_sys.system import LibrarySystem
from database_generator import DatabaseGenerator

TEST_DB_PATH = "database/test.db"

TEST_DATASET = {
    "books_data": [
            (2200, "book1", "author1", "isbn1", "publisher", 1990),
            (2201, "book2", "author2", "isbn2", "publisher", 1990),
            (2202, "book3", "author3", "isbn3", "publisher", 1990),
            (2203, "book4", "author4", "isbn4", "publisher", 1990),
            (2204, "book5", "author5", "isbn5", "publisher", 1990),
            (2205, "book6", "author6", "isbn6", "publisher", 1990),
        ],
    "customers_data": [
            (1100, "customer1"),
            (1101, "customer2"),
            (1102, "customer3"),
            (1103, "customer4"),
        ],
    "workers_data": [
            (3300, "worker1", "position"),
            (3301, "worker2", "position"),
        ],
    "queues": [
            (1100, 2200, 3300),
            (1100, 2201, 3301),
            (1101, 2201, 3301),
            (1102, 2205, 3300),
            (1103, 2205, 3300)
        ],
    "rents": [
            (2200, 1101, 3300, datetime.datetime.now() + datetime.timedelta(30)),
            (2202, 1102, 3301, datetime.datetime.now() - datetime.timedelta(2))
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
    sys.load_database(rent_if_empty=False)
    return sys


@pytest.fixture
def library_database_auto_rent():
    DatabaseGenerator(TEST_DB_PATH, test_db=True, dataset=TEST_DATASET)
    sys = LibrarySystem(database=TEST_DB_PATH)
    sys.load_database(rent_if_empty=True)
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
    result = library_simple.rent_book(0, 0, 0)
    assert result and library_simple.is_book_rented(0)


def test_rent_book_first_in_queue(library_simple):
    queue_result = library_simple.add_to_queue(0, 0, 0, rent_if_empty=False)
    rent_result = library_simple.rent_book(0, 0, 0)
    assert queue_result and rent_result and library_simple.is_book_rented(0)


def test_rent_book_in_queue(library_simple):
    library_simple.add_customer("customer")
    queue_result = library_simple.add_to_queue(1, 0, 0, rent_if_empty=False)
    rent_result = library_simple.rent_book(0, 0, 0)
    assert queue_result and not rent_result and not library_simple.is_book_rented(0)


def test_add_to_queue(library_simple):
    result = library_simple.add_to_queue(0, 0, 0, rent_if_empty=False)
    assert result and len(library_simple.books[0].queue) == 1


def test_remove_from_queue(library_simple):
    library_simple.add_to_queue(0, 0, 0, rent_if_empty=False)
    result = library_simple.remove_from_queue(0, 0)
    assert result and len(library_simple.books[0].queue) == 0


def test_try_remove_from_queue(library_simple):
    result = library_simple.remove_from_queue(0, 0)
    assert not result and len(library_simple.books[0].queue) == 0


def test_return_book(library_simple):
    library_simple.rent_book(0, 0, 0)
    library_simple.return_book(0, 0)
    assert not library_simple.is_book_rented(0)


def test_is_book_rented(library_simple):
    assert not library_simple.is_book_rented(0)


def test_get_book_due_date(library_simple):
    library_simple.rent_book(0, 0, 0)
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
    library_simple.rent_book(0, 0, 0)
    library_simple.update_date(50)
    result = library_simple.return_book(0, 0)
    assert isinstance(result, float) and result == 20 * 0.5


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


def test_rent_book_db_failed(library_database):
    result = library_database.rent_book(customer_id=TEST_DATASET["rents"][0][1], book_id=TEST_DATASET["rents"][0][0],
                                        worker_id=TEST_DATASET["rents"][0][2])
    assert (not result and
            len(library_database._cursor.execute("SELECT * FROM rents").fetchall()) == len(TEST_DATASET["rents"]))


def test_rent_book_db_successful(library_database):
    result = library_database.rent_book(customer_id=1100, book_id=2201, worker_id=TEST_DATASET["workers_data"][0][0])
    assert (result and
            len(library_database._cursor.execute("SELECT * FROM rents").fetchall()) == len(TEST_DATASET["rents"]) + 1)


def test_rent_book_db_not_firs_in_queue(library_database):
    result = library_database.rent_book(customer_id=1103, book_id=2205, worker_id=TEST_DATASET["workers_data"][0][0])
    assert (not result and
            len(library_database._cursor.execute("SELECT * FROM rents").fetchall()) == len(TEST_DATASET["rents"]))


def test_add_to_queue_db_successful(library_database):
    result = library_database.add_to_queue(customer_id=1103, book_id=2201, worker_id=TEST_DATASET["workers_data"][0][0])
    assert (result and
            len(library_database._cursor.execute("SELECT * FROM queues").fetchall()) == len(TEST_DATASET["queues"]) + 1)


def test_add_to_queue_db_failed(library_database):
    result = library_database.add_to_queue(customer_id=1103, book_id=2205, worker_id=TEST_DATASET["workers_data"][0][0])
    assert (not result and
            len(library_database._cursor.execute("SELECT * FROM queues").fetchall()) == len(TEST_DATASET["queues"]))


def test_remove_from_queue_db_successful(library_database):
    result = library_database.remove_from_queue(customer_id=TEST_DATASET["queues"][-1][0],
                                                book_id=TEST_DATASET['queues'][-1][1])
    assert (result and
            len(library_database._cursor.execute("SELECT * FROM queues").fetchall()) == len(TEST_DATASET["queues"]) - 1)


def test_remove_from_queue_db_failed(library_database):
    result = library_database.remove_from_queue(customer_id=1103, book_id=2201)
    assert (not result and
            len(library_database._cursor.execute("SELECT * FROM queues").fetchall()) == len(TEST_DATASET["queues"]))


def test_return_book_db_successful_no_fee(library_database):
    result = library_database.return_book(customer_id=1101, book_id=2200)
    assert (isinstance(result, float) and
            len(library_database._cursor.execute("SELECT * FROM rents").fetchall()) == len(TEST_DATASET["rents"]) - 1)


def test_return_book_db_successful_fee(library_database):
    result = library_database.return_book(customer_id=1102, book_id=2202)
    assert (isinstance(result, float) and result > 0 and
            len(library_database._cursor.execute("SELECT * FROM rents").fetchall()) == len(TEST_DATASET["rents"]) - 1)


def test_return_book_db_failed_wrong_customer(library_database):
    with pytest.raises(ValueError) as err:
        result = library_database.return_book(customer_id=1103, book_id=2200)
    assert len(library_database._cursor.execute("SELECT * FROM rents").fetchall()) == len(TEST_DATASET["rents"])


def test_return_book_db_failed_wrong_book(library_database):
    with pytest.raises(ValueError) as err:
        result = library_database.return_book(customer_id=1102, book_id=2201)
    assert len(library_database._cursor.execute("SELECT * FROM rents").fetchall()) == len(TEST_DATASET["rents"])


def test_is_book_rented_db_true(library_database):
    result = library_database.is_book_rented(book_id=TEST_DATASET["rents"][0][0])
    assert result


def test_is_book_rented_db_false(library_database):
    result = library_database.is_book_rented(book_id=2205)
    assert not result


def test_get_book_due_date_db_rented(library_database):
    result = library_database.get_book_due_date(book_id=TEST_DATASET["rents"][0][0])
    assert isinstance(result, datetime.datetime)


def test_get_book_due_date_db_not_rented(library_database):
    result = library_database.get_book_due_date(book_id=2205)
    assert result is None


def test_update_date_db(library_database):
    library_database.update_date()
    assert library_database.date == datetime.datetime.now()


def test_update_date_db_delta(library_database):
    initial_date = library_database.date
    library_database.update_date(20)
    assert library_database.date == (initial_date + datetime.timedelta(days=20))
