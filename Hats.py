import sqlite3
from Hat import Hat



class Hats:

    def __init__(self, conn):
        self.conn = conn

    def insert(self, hatDTO):  # insert Student DTO
        self.conn.execute("INSERT INTO hats (id,topping,supplier,quantity) VALUES (?,?,?,?)",
                          [hatDTO.id, hatDTO.topping, hatDTO.supplier, hatDTO.quantity])

    def find(self, topping):  # retrieve Student DTO
        c = self.conn.cursor()
        c.execute("""
              SELECT id, topping, supplier, quantity FROM hats WHERE topping = ?
          """, [topping, ])
        return Hat(*c.fetchone())

    def update(self, topping):
        hat = self.find(topping)
        self.conn.execute("""
                            UPDATE hats SET quantity = ? WHERE topping = ?
                              """, [(hat.quantity - 1), topping, ])
        from main import repo
        repo.conn.commit()
        hat = self.find(topping)
        if hat.quantity == 0:
            self.conn.execute("""
                    DELETE FROM hats WHERE topping=?
                      """, [topping, ])
            repo.conn.commit()
        return hat.supplier
