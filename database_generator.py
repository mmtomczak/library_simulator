import sqlite3

DEFAULT_SET = {
    "books_data": [
        (2200, 'To Kill a Mockingbird', 'Harper Lee', '9780061120084', 'J.B. Lippincott & Co.', 1960),
        (2201, 'To Kill a Mockingbird', 'Harper Lee', '9780061120084', 'J.B. Lippincott & Co.', 1960),
        (2202, 'To Kill a Mockingbird', 'Harper Lee', '9780061120084', 'J.B. Lippincott & Co.', 1960),
        (2203, 'To Kill a Mockingbird', 'Harper Lee', '9780061120084', 'J.B. Lippincott & Co.', 1960),
        (2204, 'To Kill a Mockingbird', 'Harper Lee', '9780061120084', 'J.B. Lippincott & Co.', 1960),
        (2205, '1984', 'George Orwell', '9780451524935', 'Secker & Warburg', 1949),
        (2206, '1984', 'George Orwell', '9780451524935', 'Secker & Warburg', 1949),
        (2207, '1984', 'George Orwell', '9780451524935', 'Secker & Warburg', 1949),
        (2208, '1984', 'George Orwell', '9780451524935', 'Secker & Warburg', 1949),
        (2209, '1984', 'George Orwell', '9780451524935', 'Secker & Warburg', 1949),
        (2210, 'The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', "Charles Scribner's Sons", 1925),
        (2211, 'The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', "Charles Scribner's Sons", 1925),
        (2212, 'The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', "Charles Scribner's Sons", 1925),
        (2213, 'The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', "Charles Scribner's Sons", 1925),
        (2214, 'The Great Gatsby', 'F. Scott Fitzgerald', '9780743273565', "Charles Scribner's Sons", 1925),
        (2215, 'One Hundred Years of Solitude', 'Gabriel Garcia Marquez', '9780061120091', 'Harper & Row', 1967),
        (2216, 'One Hundred Years of Solitude', 'Gabriel Garcia Marquez', '9780061120091', 'Harper & Row', 1967),
        (2217, 'One Hundred Years of Solitude', 'Gabriel Garcia Marquez', '9780061120091', 'Harper & Row', 1967),
        (2218, 'One Hundred Years of Solitude', 'Gabriel Garcia Marquez', '9780061120091', 'Harper & Row', 1967),
        (2219, 'One Hundred Years of Solitude', 'Gabriel Garcia Marquez', '9780061120091', 'Harper & Row', 1967),
        (2220, 'Brave New World', 'Aldous Huxley', '9780060850524', 'Chatto & Windus', 1932),
        (2221, 'Brave New World', 'Aldous Huxley', '9780060850524', 'Chatto & Windus', 1932),
        (2222, 'Brave New World', 'Aldous Huxley', '9780060850524', 'Chatto & Windus', 1932),
        (2223, 'Brave New World', 'Aldous Huxley', '9780060850524', 'Chatto & Windus', 1932),
        (2224, 'Brave New World', 'Aldous Huxley', '9780060850524', 'Chatto & Windus', 1932),
        (2225, 'The Catcher in the Rye', 'J.D. Salinger', '9780316769480', 'Little, Brown and Company', 1951),
        (2226, 'The Catcher in the Rye', 'J.D. Salinger', '9780316769480', 'Little, Brown and Company', 1951),
        (2227, 'The Catcher in the Rye', 'J.D. Salinger', '9780316769480', 'Little, Brown and Company', 1951),
        (2228, 'The Catcher in the Rye', 'J.D. Salinger', '9780316769480', 'Little, Brown and Company', 1951),
        (2229, 'The Catcher in the Rye', 'J.D. Salinger', '9780316769480', 'Little, Brown and Company', 1951),
        (2230, 'To the Lighthouse', 'Virginia Woolf', '9780156907392', 'Hogarth Press', 1927),
        (2231, 'To the Lighthouse', 'Virginia Woolf', '9780156907392', 'Hogarth Press', 1927),
        (2232, 'To the Lighthouse', 'Virginia Woolf', '9780156907392', 'Hogarth Press', 1927),
        (2233, 'To the Lighthouse', 'Virginia Woolf', '9780156907392', 'Hogarth Press', 1927),
        (2234, 'To the Lighthouse', 'Virginia Woolf', '9780156907392', 'Hogarth Press', 1927),
        (2235, 'The Lord of the Rings', 'J.R.R. Tolkien', '9780544003415', 'George Allen & Unwin', 1954),
        (2236, 'The Lord of the Rings', 'J.R.R. Tolkien', '9780544003415', 'George Allen & Unwin', 1954),
        (2237, 'The Lord of the Rings', 'J.R.R. Tolkien', '9780544003415', 'George Allen & Unwin', 1954),
        (2238, 'The Lord of the Rings', 'J.R.R. Tolkien', '9780544003415', 'George Allen & Unwin', 1954),
        (2239, 'The Lord of the Rings', 'J.R.R. Tolkien', '9780544003415', 'George Allen & Unwin', 1954),
        (2240, 'Pride and Prejudice', 'Jane Austen', '9780141439518', 'T. Egerton, Whitehall', 1813),
        (2241, 'Pride and Prejudice', 'Jane Austen', '9780141439518', 'T. Egerton, Whitehall', 1813),
        (2242, 'Pride and Prejudice', 'Jane Austen', '9780141439518', 'T. Egerton, Whitehall', 1813),
        (2243, 'Pride and Prejudice', 'Jane Austen', '9780141439518', 'T. Egerton, Whitehall', 1813),
        (2244, 'Pride and Prejudice', 'Jane Austen', '9780141439518', 'T. Egerton, Whitehall', 1813),
        (2245, 'The Road', 'Cormac McCarthy', '9780307387899', 'Knopf', 2006),
        (2246, 'The Road', 'Cormac McCarthy', '9780307387899', 'Knopf', 2006),
        (2247, 'The Road', 'Cormac McCarthy', '9780307387899', 'Knopf', 2006),
        (2248, 'The Road', 'Cormac McCarthy', '9780307387899', 'Knopf', 2006),
        (2249, 'The Road', 'Cormac McCarthy', '9780307387899', 'Knopf', 2006),
        (2250, 'The Chronicles of Narnia', 'C.S. Lewis', '9780066238500', 'Geoffrey Bles', 1950),
        (2251, 'The Chronicles of Narnia', 'C.S. Lewis', '9780066238500', 'Geoffrey Bles', 1950),
        (2252, 'The Chronicles of Narnia', 'C.S. Lewis', '9780066238500', 'Geoffrey Bles', 1950),
        (2253, 'The Chronicles of Narnia', 'C.S. Lewis', '9780066238500', 'Geoffrey Bles', 1950),
        (2254, 'The Chronicles of Narnia', 'C.S. Lewis', '9780066238500', 'Geoffrey Bles', 1950),
        (2255, 'Moby-Dick', 'Herman Melville', '9780142437247', 'Harper & Brothers', 1851),
        (2256, 'Moby-Dick', 'Herman Melville', '9780142437247', 'Harper & Brothers', 1851),
        (2257, 'Moby-Dick', 'Herman Melville', '9780142437247', 'Harper & Brothers', 1851),
        (2258, 'Moby-Dick', 'Herman Melville', '9780142437247', 'Harper & Brothers', 1851),
        (2259, 'Moby-Dick', 'Herman Melville', '9780142437247', 'Harper & Brothers', 1851),
        (2260, 'Wuthering Heights', 'Emily Brontë', '9780141439556', 'Thomas Cautley Newby', 1847),
        (2261, 'Wuthering Heights', 'Emily Brontë', '9780141439556', 'Thomas Cautley Newby', 1847),
        (2262, 'Wuthering Heights', 'Emily Brontë', '9780141439556', 'Thomas Cautley Newby', 1847),
        (2263, 'Wuthering Heights', 'Emily Brontë', '9780141439556', 'Thomas Cautley Newby', 1847),
        (2264, 'Wuthering Heights', 'Emily Brontë', '9780141439556', 'Thomas Cautley Newby', 1847),
        (2265, "The Hitchhiker's Guide to the Galaxy", 'Douglas Adams', '9780345391803', 'Pan Books', 1979),
        (2266, "The Hitchhiker's Guide to the Galaxy", 'Douglas Adams', '9780345391803', 'Pan Books', 1979),
        (2267, "The Hitchhiker's Guide to the Galaxy", 'Douglas Adams', '9780345391803', 'Pan Books', 1979),
        (2268, "The Hitchhiker's Guide to the Galaxy", 'Douglas Adams', '9780345391803', 'Pan Books', 1979),
        (2269, "The Hitchhiker's Guide to the Galaxy", 'Douglas Adams', '9780345391803', 'Pan Books', 1979),
        (2270, 'The Grapes of Wrath', 'John Steinbeck', '9780143039433', 'The Viking Press', 1939),
        (2271, 'The Grapes of Wrath', 'John Steinbeck', '9780143039433', 'The Viking Press', 1939),
        (2272, 'The Grapes of Wrath', 'John Steinbeck', '9780143039433', 'The Viking Press', 1939),
        (2273, 'The Grapes of Wrath', 'John Steinbeck', '9780143039433', 'The Viking Press', 1939),
        (2274, 'The Grapes of Wrath', 'John Steinbeck', '9780143039433', 'The Viking Press', 1939),
        (2275, 'Frankenstein', 'Mary Shelley', '9780486282114', 'Lackington, Hughes, Harding, Mavor & Jones', 1818),
        (2276, 'Frankenstein', 'Mary Shelley', '9780486282114', 'Lackington, Hughes, Harding, Mavor & Jones', 1818),
        (2277, 'Frankenstein', 'Mary Shelley', '9780486282114', 'Lackington, Hughes, Harding, Mavor & Jones', 1818),
        (2278, 'Frankenstein', 'Mary Shelley', '9780486282114', 'Lackington, Hughes, Harding, Mavor & Jones', 1818),
        (2279, 'Frankenstein', 'Mary Shelley', '9780486282114', 'Lackington, Hughes, Harding, Mavor & Jones', 1818),
        (2280, 'The Scarlet Letter', 'Nathaniel Hawthorne', '9780142437261', 'Ticknor, Reed & Fields', 1850),
        (2281, 'The Scarlet Letter', 'Nathaniel Hawthorne', '9780142437261', 'Ticknor, Reed & Fields', 1850),
        (2282, 'The Scarlet Letter', 'Nathaniel Hawthorne', '9780142437261', 'Ticknor, Reed & Fields', 1850),
        (2283, 'The Scarlet Letter', 'Nathaniel Hawthorne', '9780142437261', 'Ticknor, Reed & Fields', 1850),
        (2284, 'The Scarlet Letter', 'Nathaniel Hawthorne', '9780142437261', 'Ticknor, Reed & Fields', 1850),
        (2285, 'The Shining', 'Stephen King', '9780307743657', 'Doubleday', 1977),
        (2286, 'The Shining', 'Stephen King', '9780307743657', 'Doubleday', 1977),
        (2287, 'The Shining', 'Stephen King', '9780307743657', 'Doubleday', 1977),
        (2288, 'The Shining', 'Stephen King', '9780307743657', 'Doubleday', 1977),
        (2289, 'The Shining', 'Stephen King', '9780307743657', 'Doubleday', 1977),
        (2290, 'Crime and Punishment', 'Fyodor Dostoevsky', '9780143107637', 'The Russian Messenger', 1866),
        (2291, 'Crime and Punishment', 'Fyodor Dostoevsky', '9780143107637', 'The Russian Messenger', 1866),
        (2292, 'Crime and Punishment', 'Fyodor Dostoevsky', '9780143107637', 'The Russian Messenger', 1866),
        (2293, 'Crime and Punishment', 'Fyodor Dostoevsky', '9780143107637', 'The Russian Messenger', 1866),
        (2294, 'Crime and Punishment', 'Fyodor Dostoevsky', '9780143107637', 'The Russian Messenger', 1866),
        (2295, 'The Picture of Dorian Gray', 'Oscar Wilde', '9780141439570', 'Ward, Lock and Company', 1890),
        (2296, 'The Picture of Dorian Gray', 'Oscar Wilde', '9780141439570', 'Ward, Lock and Company', 1890),
        (2297, 'The Picture of Dorian Gray', 'Oscar Wilde', '9780141439570', 'Ward, Lock and Company', 1890),
        (2298, 'The Picture of Dorian Gray', 'Oscar Wilde', '9780141439570', 'Ward, Lock and Company', 1890),
        (2299, 'The Picture of Dorian Gray', 'Oscar Wilde', '9780141439570', 'Ward, Lock and Company', 1890)
    ],
    "customers_data": [
        (1100, 'Alice'),
        (1101, 'Bob'),
        (1102, 'Charlie'),
        (1103, 'David'),
        (1104, 'Eva'),
        (1105, 'Frank'),
        (1106, 'Grace'),
        (1107, 'Harry'),
        (1108, 'Ivy'),
        (1109, 'Jack'),
        (1110, 'Katie'),
        (1111, 'Liam'),
        (1112, 'Mia'),
        (1113, 'Noah'),
        (1114, 'Olivia'),
        (1115, 'Penny'),
        (1116, 'Quinn'),
        (1117, 'Ryan'),
        (1118, 'Sophie'),
        (1119, 'Tyler')
    ],
    "workers_data": [
        (3300, "John", "Librarian"),
        (3301, "Emily", "Librarian"),
        (3302, "David", "Librarian"),
        (3303, "Sophie", "Librarian"),
        (3304, "James", "Librarian"),
        (3305, "Olivia", "Librarian"),
        (3306, "William", "Librarian"),
        (3307, "Emma", "Librarian"),
        (3308, "Michael", "Librarian"),
        (3309, "Isabella", "Librarian")
    ]
}


class DatabaseGenerator:
    """
    Creates or clears SQLite database in the declared location. Inserts supplied data into the database.

    Args:
        db_path (str): location of the database/where database is to be created
        test_db (bool): sets the generator into the test mode, defaults to False
        dataset: dataset that is to be inserted into the database

    Keyword Args:
        clear_data (bool): defines if data in the dataset is to be cleared, defaults to True
        drop_tables (bool): defines if the tables in the dataset are to be dropped, defaults to True
        generate (bool): defines if the database is to be generated, defaults to True
        insert_sample (bool): defines if sample data is to be inserted into the database, defaults to True

    Attributes:
        path (str): path to the database
        dataset: dataset that is to be inserted into the database
    """
    def __init__(self, db_path: str, test_db: bool = False, dataset=None, **kwargs):
        if dataset is None:
            dataset = DEFAULT_SET

        self.path = db_path
        self.dataset = dataset
        if kwargs.get("clear_data", True):
            try:
                self.clear_data()
            except sqlite3.OperationalError:
                pass
        if kwargs.get("drop_tables", True):
            try:
                self.drop_tables()
            except sqlite3.OperationalError:
                pass
        if kwargs.get("generate", True):
            self.generate_database()
        if kwargs.get("insert_sample", True):
            self.insert_sample_data()
        if test_db:
            self.insert_test_scenarios()

    def insert_sample_data(self):
        """
        Inserts sample data into the database
        """
        con = sqlite3.connect(self.path)
        cur = con.cursor()
        try:
            cur.executemany("""
                            INSERT INTO books(book_id, title, author, isbn, publisher, year_published) 
                            VALUES(?, ?, ?, ?, ?, ?)
                            """,
                            self.dataset["books_data"])

            cur.executemany("INSERT INTO workers(worker_id, name, position) VALUES(?, ?, ?)",
                            self.dataset["workers_data"])

            cur.executemany("INSERT INTO customers(customer_id, name) VALUES(?, ?)",
                            self.dataset["customers_data"])
        except sqlite3.IntegrityError as err:
            print(f"\nERROR LOADING DATABASE\n{err}\nCLEARING DATA")
            self.clear_data()
        con.commit()
        con.close()

    def generate_database(self):
        """
        Generates the database
        """
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
            worker_id INTEGER NOT NULL,
            return_date TEXT NOT NULL,
            FOREIGN KEY (book_id) REFERENCES books(book_id),
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id))
            ''')

        cur.execute('''
            CREATE TABLE queues(
                entry_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                worker_id INTEGER NOT NULL,
                customer_id INTEGER NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(book_id),
                FOREIGN KEY (customer_id) REFERENCES customers(customer_id))
                ''')

        con.commit()
        con.close()

    def clear_data(self):
        """
        Clears the data from the database
        """
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
        """
        Drops the tables from the database
        """
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
        """
        Inserts test scenarios into the database
        """
        con = sqlite3.connect(self.path)
        cur = con.cursor()

        cur.executemany("INSERT INTO queues(customer_id, book_id, worker_id) VALUES(?,?,?)", self.dataset["queues"])
        cur.executemany("INSERT INTO rents(book_id, customer_id, worker_id, return_date) VALUES(?,?,?, ?)", self.dataset["rents"])

        con.commit()
        con.close()


