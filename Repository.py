import sqlite3
from Hats import Hats
from Suppliers import Suppliers
from Orders import Orders


class Repository:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.hats = Hats(self.conn)  # DAO for students table
        self.suppliers = Suppliers(self.conn)  # DAO for assignments table
        self.orders = Orders(self.conn)  # DAO for grades table

    def create_tables(self):
        self.conn.executescript("CREATE TABLE hats (id INTEGER PRIMARY KEY, topping STRING NOT "
                                "NULL, supplier INTEGER REFERENCES suppliers(id), quantity INTEGER NOT NULL); "
                                "CREATE TABLE suppliers(id INTEGER PRIMARY KEY, name STRING NOT NULL); "
                                "CREATE TABLE orders(id INTEGER PRIMARY KEY, "
                                "location STRING NOT NULL, hat INTEGER REFERENCES hats(id));")

    def close(self):
        self.conn.commit()
        self.conn.close()
