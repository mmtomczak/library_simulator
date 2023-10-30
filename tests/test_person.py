import pytest

from person import Person, Worker, Customer

SAMPLE_PERSON = {"name": "person",
                 "id": 111}
SAMPLE_WORKER = {**SAMPLE_PERSON,
                 "position": "position"}
SAMPLE_CUSTOMER = {**SAMPLE_PERSON}


# PERSON TESTS
@pytest.fixture
def person():
    return Person(**SAMPLE_PERSON)


def test_name_getter(person):
    assert person.name == SAMPLE_PERSON["name"]


def test_name_setter(person):
    person.name = "new name"
    assert person.name == "new name"


def test_id_getter(person):
    assert person.id == SAMPLE_PERSON["id"]


def test_id_setter(person):
    person.id = 999
    assert person.id == 999


# WORKER TESTS
@pytest.fixture()
def worker():
    return Worker(**SAMPLE_WORKER)


def test_position_getter(worker):
    assert worker.position == SAMPLE_WORKER["position"]


def test_position_setter(worker):
    worker.position = "new position"
    assert worker.position == "new position"


# CUSTOMER TESTS
@pytest.fixture
def customer():
    return Customer(**SAMPLE_CUSTOMER)


def test_return_book_one(customer):
    customer.rent_book("book object")
    customer.return_book("book object")
    assert customer.rented_books == []


def test_return_book_multiple(customer):
    customer.rent_book("book object 1")
    customer.rent_book("book object 2")
    customer.rent_book("book object 3")
    customer.rent_book("book object 4")
    customer.return_book("book object 2")
    customer.return_book("book object 4")
    assert customer.rented_books == ["book object 1", "book object 3"]
