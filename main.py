from Simulation import Simulation
from database_generator import DatabaseGenerator
import datetime


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

DatabaseGenerator("tests/database/test.db", test_db=True, dataset=TEST_DATASET)
sim = Simulation(db_path="database/library.db")
sim.system.load_database()
print(sim.books[-1].title)
print(sim.system._new_book_id)
# sim.system.rent_book(3301, 2206)
#
# # TODO Simulation class
# # TODO User interface class
#
# # TODO setup tests
#
# io = Simulation()
# io.add_book(**{'title':'Catcher in the rye', 'author':'Some guy', 'iban':'AV387921873', 'publisher':'publisher', 'year_published':1111})
# print(io.system.books)

