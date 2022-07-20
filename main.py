# import sqlite3 library
import atexit
import os
import sqlite3
import sys


class Repository:
    def __init__(self):
        self.conn = sqlite3.connect(sys.argv[4]) # 4
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


class Hats:

    def __init__(self, conn):
        self.conn = conn

    def insert(self, hatDTO):  # insert Student DTO
        self.conn.execute("INSERT INTO hats (id,topping,supplier,quantity) VALUES (?,?,?,?)",
                          [hatDTO.id, hatDTO.topping, hatDTO.supplier, hatDTO.quantity])

    def find(self, topping):  # retrieve Student DTO
        c = self.conn.cursor()
        m=c.execute("""
              SELECT * FROM hats WHERE topping = ? 
          """, [topping]).fetchall()

        min = int(m[0][2])
        minRec = m[0]
        for s in m:
            if int(s[2]) < min:
                min = int(s[2])
                minRec = s
        print(minRec)
        return Hat(*minRec)

    def update(self, topping):
        hat = self.find(topping)
        self.conn.execute("""
                            UPDATE hats SET quantity = ? WHERE id=?
                              """, [(hat.quantity - 1), hat.id, ])
        repo.conn.commit()
        hat = self.find(topping)
        if hat.quantity == 0:
            self.conn.execute("""
                    DELETE FROM hats WHERE id=?
                      """, [hat.id, ])
            repo.conn.commit()
        return hat


class Hat:

    def __init__(self, id, topping, supplier, quantity):
        self.id = id
        self.topping = topping
        self.supplier = supplier
        self.quantity = quantity


class Orders:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, orderDTO):  # insert Student DTO
        self.conn.execute("""
               INSERT INTO orders (id, location, hat) VALUES (?, ?, ?)
           """, [orderDTO.id, orderDTO.location, orderDTO.hat])

    def find(self, id):  # retrieve Student DTO
        c = self.conn.cursor()
        c.execute("""
            SELECT id, location, hat FROM orders WHERE id = ?
        """, [id, ])
        return Order(*c.fetchone())


class Supplier:

    def __init__(self, id, name):
        self.id = id
        self.name = name


class Suppliers:
    def __init__(self, conn):
        self.conn = conn

    def insert(self, supplierDTO):  # insert Student DTO
        self.conn.execute("""
               INSERT INTO suppliers (id, name) VALUES (?, ?)
           """, [supplierDTO.id, supplierDTO.name])

    def find(self, id):  # retrieve Student DTO
        c = self.conn.cursor()
        c.execute("""
            SELECT id, name FROM suppliers WHERE id = ?
        """, [id])
        return Supplier(*c.fetchone())


class Order:

    def __init__(self, id, location, hat):
        self.id = id
        self.location = location
        self.hat = hat


idcounter = 1


def execute(location, topping):
    global idcounter
    hat = repo.hats.update(topping)
    supplier=hat.supplier
    suppliername = repo.suppliers.find(supplier).name
    order = Order(idcounter, location, hat.id)
    idcounter = idcounter + 1
    repo.orders.insert(order)
    repo.conn.commit()
    f = open(sys.argv[3], "a") # 3
    f.write(str(topping) + "," + suppliername + "," + location + '\n')
    f.close()


def main(_args):
    global repo
    # create repository singleton
    repo.create_tables()

    # parsing config and orders files
    parsing_config(repo)

    parsing_orders(repo)
    atexit.register(repo.close)
    # close


def parsing_config(repo):
    hats_num = 0
    suppliers_num = 0
    with open(sys.argv[1], 'r') as file1: # 1
        for i, line in enumerate(file1):
            tmp_line = line.rstrip()
            tmp_line = tmp_line.split(',')
            if i == 0:
                hats_num = int(tmp_line[0])
                suppliers_num = int(tmp_line[1])
            elif hats_num != 0:
                hats_num = hats_num - 1
                hat = Hat(int(tmp_line[0]), str(tmp_line[1]), int(tmp_line[2]), int(tmp_line[3]))
                repo.hats.insert(hat)
            elif suppliers_num != 0:
                suppliers_num = suppliers_num - 1
                supplier = Supplier(tmp_line[0], tmp_line[1])
                repo.suppliers.insert(supplier)
    repo.conn.commit()


def parsing_orders(repo):
    with open(sys.argv[2], 'r') as file1: # 2
        for i, line in enumerate(file1):
            tmp_line = line.rstrip()
            tmp_line = tmp_line.split(',')
            execute(tmp_line[0], tmp_line[1])


repo = Repository()
if __name__ == '__main__':
    main(sys.argv)
