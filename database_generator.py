import sqlite3

DEFAULT_SET = {
    "books_data": [
            (2200, "War and Peace", "Leo Tolstoy", "AA123456789", "Publisher Placeholder", 1990),
            (2201, "War and Peace", "Leo Tolstoy", "AA123456789", "Publisher Placeholder", 1990),
            (2202, "War and Peace", "Leo Tolstoy", "AA123456789", "Publisher Placeholder", 1990),
            (2203, "War and Peace", "Leo Tolstoy", "AA123456789", "Publisher Placeholder", 1990),
            (2204, "War and Peace", "Leo Tolstoy", "AA123456789", "Publisher Placeholder", 1990),
            (2205, "The Catcher in the Rye", "J.D. Salinger", "BB123456789", "Publisher Placeholder", 1990),
            (2206, "The Catcher in the Rye", "J.D. Salinger", "BB123456789", "Publisher Placeholder", 1990),
            (2207, "The Catcher in the Rye", "J.D. Salinger", "BB123456789", "Publisher Placeholder", 1990),
            (2208, "The Catcher in the Rye", "J.D. Salinger", "BB123456789", "Publisher Placeholder", 1990),
            (2209, "The Catcher in the Rye", "J.D. Salinger", "BB123456789", "Publisher Placeholder", 1990),
        ],
    "customers_data": [
            (3300, "Mike"),
            (3301, "John"),
            (3302, "Julia"),
            (3303, "Anna"),
            (3304, "Aron"),
            (3305, "Jack"),
            (3306, "Sully"),
        ],
    "workers_data": [
            (1100, "John", "Librarian"),
            (1101, "Michael", "Librarian"),
            (1102, "Jenny", "Librarian"),
            (1103, "Natalie", "Librarian"),
            (1104, "Erwin", "Librarian"),
            (1105, "Juliet", "Librarian"),
        ]
}


class DatabaseGenerator:
    def __init__(self, db_path: str, test_db: bool = False, dataset=None):
        if dataset is None:
            dataset = DEFAULT_SET

        self.path = db_path
        self.dataset = dataset
        try:
            self.clear_data()
        except sqlite3.OperationalError:
            pass
        try:
            self.drop_tables()
        except sqlite3.OperationalError:
            pass
        self.generate_database()
        self.insert_sample_data()
        if test_db:
            self.insert_test_scenarios()

    def insert_sample_data(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()

        cur.executemany("""
                        INSERT INTO books(book_id, title, author, isbn, publisher, year_published) 
                        VALUES(?, ?, ?, ?, ?, ?)
                        """,
                        self.dataset["books_data"])

        cur.executemany("INSERT INTO workers(worker_id, name, position) VALUES(?, ?, ?)",
                        self.dataset["workers_data"])

        cur.executemany("INSERT INTO customers(customer_id, name) VALUES(?, ?)",
                        self.dataset["customers_data"])

        con.commit()
        con.close()

    def generate_database(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()

        cur.execute('''
        CREATE TABLE books(
            book_id INTEGER NOT NULL PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT,
            isbn TEXT,
            publisher TEXT,
            year_published INTEGER)
        ''')

        cur.execute('''
        CREATE TABLE workers(
            worker_id INTEGER NOT NULL PRIMARY KEY ,
            name TEXT NOT NULL,
            position TEXT)
        ''')

        cur.execute('''
        CREATE TABLE customers(
            customer_id INTEGER NOT NULL PRIMARY KEY ,
            name TEXT NOT NULL)
        ''')

        cur.execute('''
        CREATE TABLE rents(
            rent_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            customer_id INTEGER NOT NULL,
            return_date TEXT NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id))
            ''')

        cur.execute('''
            CREATE TABLE queues(
                entry_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(book_id),
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id))
                ''')

        con.commit()
        con.close()

    def clear_data(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()

        cur.execute("DELETE FROM books")
        cur.execute("DELETE FROM workers")
        cur.execute("DELETE FROM customers")
        cur.execute("DELETE FROM rents")
        cur.execute("DELETE FROM queues")

        con.commit()
        con.close()

    def drop_tables(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()

        cur.execute("DROP TABLE books")
        cur.execute("DROP TABLE workers")
        cur.execute("DROP TABLE customers")
        cur.execute("DROP TABLE rents")
        cur.execute("DROP TABLE queues")

        con.commit()
        con.close()

    def insert_test_scenarios(self):
        con = sqlite3.connect(self.path)
        cur = con.cursor()

        cur.executemany("INSERT INTO queues(customer_id, book_id) VALUES(?,?)", self.dataset["queues"])
        cur.executemany("INSERT INTO rents(book_id, customer_id, return_date) VALUES(?,?,?)", self.dataset["rents"])

        con.commit()
        con.close()


